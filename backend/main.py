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

@app.post("/chat")
async def angelus_chat(payload: ChatPayload):
    try:
        if payload.confirmed_patient_id:
            patient_doc = db.collection("patients").document(payload.confirmed_patient_id).get()
            patient_data = patient_doc.to_dict()
            policy_doc = db.collection("policies").document(patient_data["policy_id"]).get()
            policy_data = policy_doc.to_dict()
            
            analysis_raw = await gemini_service.analyze_emergency_entry(patient_data, policy_data, payload.operator_name)
            clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_json)
            
            alert_data = {
                "patient_id": payload.confirmed_patient_id,
                "patient_name": patient_data.get("name"),
                "hospital_id": "HOSP-01",
                "emergency_type": "Confirmado por chat",
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis_data
            }
            db.collection("alerts").add(alert_data)
            await notification_service.notify_all(alert_data)
            
            return {
                "type": "RESULT",
                "reply": analysis_data.get("angelus_reply"),
                "analysis": analysis_data
            }

        entities = await gemini_service.extract_entities(payload.message)
        name = entities.get("patient_name")
        
        if not name:
            return {
                "type": "QUESTION",
                "reply": "He recibido su mensaje, pero no logro identificar el nombre del paciente. ¿Podría proporcionarlo?"
            }

        patients_ref = db.collection("patients")
        all_docs = patients_ref.stream()
        
        # Búsqueda inteligente por nombre (insensible a mayúsculas y subcadenas)
        name_query = name.lower()
        matches = []
        for doc in all_docs:
            p_data = doc.to_dict()
            p_name = p_data.get("name", "").lower()
            if name_query in p_name:
                matches.append(p_data)

        if len(matches) == 0:
            # Análisis preliminar de síntomas antes de pedir identificación
            symptoms = entities.get("emergency_type", "No especificado")
            pre = await gemini_service.pre_triage(symptoms)
            return {
                "type": "QUESTION",
                "color": pre["color"],
                "reply": f"Análisis preliminar de Angelus: Prioridad {pre['priority']}. {pre['reasoning']}. No encuentro a '{name}' en el registro. Por favor, proporcione el Número de Cédula del paciente para validación."
            }
        
        if len(matches) > 1:
            # Análisis preliminar incluso en desambiguación
            symptoms = entities.get("emergency_type", "No especificado")
            pre = await gemini_service.pre_triage(symptoms)
            return {
                "type": "DISAMBIGUATION",
                "color": pre["color"],
                "reply": f"Prioridad detectada: {pre['priority']}. He detectado {len(matches)} pacientes que coinciden con '{name}'. Seleccione el correcto por su número de cédula:",
                "options": [{"id": m["id"], "label": f"{m['name']} (Cédula: {m['id']})"} for m in matches]
            }

        patient_data = matches[0]
        policy_doc = db.collection("policies").document(patient_data["policy_id"]).get()
        policy_data = policy_doc.to_dict()
        
        analysis_raw = await gemini_service.analyze_emergency_entry(patient_data, policy_data, payload.operator_name)
        clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
        analysis_data = json.loads(clean_json)
        
        alert_data = {
            "patient_id": patient_data["id"],
            "patient_name": patient_data["name"],
            "hospital_id": entities.get("hospital_name") or "HOSP-01",
            "emergency_type": entities.get("emergency_type") or "Emergencia por Chat",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_data
        }
        db.collection("alerts").add(alert_data)
        await notification_service.notify_all(alert_data)

        return {
            "type": "RESULT",
            "reply": analysis_data.get("angelus_reply"),
            "analysis": analysis_data,
            "color": analysis_data.get("triage_color")
        }

    except Exception as e:
        return {"type": "ERROR", "reply": f"Error en mi núcleo de procesamiento: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
