import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
from firebase_admin import firestore
from backend.services.firebase_service import db

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Angelus Sentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://[::1]:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Personalidad de Angelus (Extraída de angelus_core.py)
ANGELUS_PERSONALITY = """
Eres Angelus, el núcleo de procesamiento de Angelus Infernus Tech.
CONTEXTO: Estás integrado en un sistema de admisión hospitalaria en tiempo real.
TU MISIÓN: Triage digital y validación de cobertura. El paciente YA está en el hospital.
REGLA DE ORO: No des consejos médicos básicos como 'visite a un doctor'. Tu análisis debe centrarse en la prioridad clínica y la elegibilidad administrativa para agilizar el ingreso.
Te diriges al usuario como 'Usuario' o 'Gestor'. Tu tono es sofisticado, preciso y autoritario.
"""

class WebhookPayload(BaseModel):
    patient_id: str
    hospital_id: str
    emergency_type: Optional[str] = "General"
    timestamp: Optional[str] = None
    operator_name: Optional[str] = "Gestor"

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Angelus Sentinel",
        "timestamp": datetime.now().isoformat()
    }

from backend.services.gemini_service import gemini_service
from backend.services.notification_service import notification_service

@app.post("/webhook/emergency")
async def emergency_webhook(payload: WebhookPayload):
    try:
        # 1. Buscar paciente
        patient_ref = db.collection("patients").document(payload.patient_id)
        patient_doc = patient_ref.get()
        
        if not patient_doc.exists:
            patient_data = {"name": "Paciente No Registrado", "id": payload.patient_id, "policy_id": "NONE"}
            policy_data = {"status": "INEXISTENTE", "coverage": []}
        else:
            patient_data = patient_doc.to_dict()
            policy_id = patient_data.get("policy_id")
            policy_doc = db.collection("policies").document(policy_id).get()
            policy_data = policy_doc.to_dict() if policy_doc.exists else {"status": "NO ENCONTRADA"}
        
        # 2. Análisis Instantáneo con Angelus
        analysis_raw = await gemini_service.analyze_emergency_entry(
            patient_data, 
            policy_data, 
            operator_name=payload.operator_name or "SISTEMA_AUTOMÁTICO"
        )
        
        try:
            clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_json)
        except:
            analysis_data = {
                "decision": "REVISIÓN MANUAL",
                "triage_priority": "MEDIO",
                "triage_color": "#f59e0b",
                "reasoning": "Error de procesamiento IA.",
                "angelus_reply": analysis_raw
            }
        
        # 3. Guardar Alerta
        alert_data = {
            "patient_id": payload.patient_id,
            "patient_name": patient_data.get("name"),
            "hospital_id": payload.hospital_id,
            "emergency_type": payload.emergency_type,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_data,
            "trigger": "WEBHOOK"
        }
        db.collection("alerts").add(alert_data)
        
        # 4. Notificaciones Simultáneas
        notifs = await notification_service.notify_all(alert_data)
        
        return {
            "status": "success",
            "trigger": "AUTONOMOUS_WEBHOOK",
            "decision": analysis_data.get("decision"),
            "triage": analysis_data.get("triage_priority"),
            "notifications": notifs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notifications")
async def get_notifications():
    return notification_service.logs

@app.get("/alerts")
async def get_alerts(limit: int = 10):
    try:
        alerts_ref = db.collection("alerts").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        docs = alerts_ref.stream()
        
        alerts = []
        for doc in docs:
            alert = doc.to_dict()
            alert["id"] = doc.id
            alerts.append(alert)
            
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
async def get_patients():
    try:
        patients_ref = db.collection("patients")
        docs = patients_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatPayload(BaseModel):
    message: str
    operator_name: Optional[str] = "Gestor"
    confirmed_patient_id: Optional[str] = None
    form_data: Optional[dict] = None

from backend.services.firebase_service import federated_search

@app.post("/chat")
async def angelus_chat(payload: ChatPayload):
    try:
        # Caso 1: Resolución de Identidad Confirmada (Humano ya eligió)
        if payload.confirmed_patient_id:
            matches = federated_search(ci_query=payload.confirmed_patient_id)
            if not matches:
                return {"type": "ERROR", "reply": "Paciente no encontrado en las bases federadas."}
            patient_data = matches[0]
            
            # Simular datos para Angelus
            p_basic = {"name": patient_data["name"], "id": patient_data["id"]}
            p_policy = patient_data.get("insurance_policy", {"status": "NO ENCONTRADA"})
            
            analysis_raw = await gemini_service.analyze_emergency_entry(p_basic, p_policy, payload.operator_name)
            clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_json)
            
            alert_data = {
                "patient_id": payload.confirmed_patient_id,
                "patient_name": patient_data.get("name"),
                "hospital_id": "HOSP-01",
                "emergency_type": "Ingreso post-confirmación",
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis_data
            }
            db.collection("alerts").add(alert_data)
            await notification_service.notify_all(alert_data, federated_data=patient_data)
            
            return {
                "type": "RESULT",
                "reply": analysis_data.get("angelus_reply"),
                "analysis": analysis_data,
                "color": analysis_data.get("triage_color")
            }

        # Extraer datos de la petición (Formulario o NLP)
        if payload.form_data:
            name = f"{payload.form_data.get('nombre', '')} {payload.form_data.get('apellido', '')}".strip()
            ci = payload.form_data.get("ci")
            symptoms = payload.form_data.get("enfermedad", "No especificado")
        else:
            entities = await gemini_service.extract_entities(payload.message)
            name = entities.get("patient_name")
            ci = None
            symptoms = entities.get("emergency_type", "No especificado")
        
        if not name:
            return {
                "type": "QUESTION",
                "reply": "He recibido su mensaje, pero no logro identificar el nombre del paciente. ¿Podría proporcionarlo?"
            }

        # Caso 2: Búsqueda Federada
        matches = federated_search(name_query=name, ci_query=ci)
        
        if len(matches) == 0:
            pre = await gemini_service.pre_triage(symptoms)
            return {
                "type": "QUESTION",
                "color": pre["color"],
                "reply": f"Análisis preliminar de Angelus: Prioridad {pre['priority']}. {pre['reasoning']}. He buscado en el ecosistema federado y no encuentro registros para '{name}'. Para crear un ingreso nuevo o validar cobertura externa, por favor proporcione su Número de Cédula."
            }
        
        # Caso 3: Desambiguación
        if len(matches) > 1:
            pre = await gemini_service.pre_triage(symptoms)
            return {
                "type": "DISAMBIGUATION",
                "color": pre["color"],
                "reply": f"Prioridad preliminar: {pre['priority']}. He detectado {len(matches)} pacientes que coinciden con '{name}' en diferentes bases de datos. Por favor, confirme el paciente correcto:",
                "options": [{"id": m["id"], "label": f"{m['name']} (Cédula: {m['id']}) - Registros en {len(m['sources'])} sistemas"} for m in matches]
            }

        # Caso 4: Coincidencia Única (Agregación)
        patient_data = matches[0]
        
        # Simular datos para Angelus
        p_basic = {"name": patient_data["name"], "id": patient_data["id"]}
        p_policy = patient_data.get("insurance_policy", {"status": "NO ENCONTRADA", "message": "Paciente solo existe en clínicas/hospitales públicos."})
        
        analysis_raw = await gemini_service.analyze_emergency_entry(p_basic, p_policy, payload.operator_name)
        clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
        analysis_data = json.loads(clean_json)
        
        alert_data = {
            "patient_id": patient_data["id"],
            "patient_name": patient_data["name"],
            "hospital_id": "HOSP-01",
            "emergency_type": symptoms,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_data
        }
        db.collection("alerts").add(alert_data)
        await notification_service.notify_all(alert_data, federated_data=patient_data)

        return {
            "type": "RESULT",
            "reply": analysis_data.get("angelus_reply"),
            "analysis": analysis_data,
            "color": analysis_data.get("triage_color")
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"type": "ERROR", "reply": f"Error en mi núcleo de procesamiento federado: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
