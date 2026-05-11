import sys
import os
import json
from datetime import datetime

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import FastAPI app
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import backend functions
from main import (
    _validate_policy_async, 
    _check_preexisting_conditions_async, 
    _send_simultaneous_notifications,
    notification_service,
    db
)

app = FastAPI(title="Angelus Sentinel API - Admision")

class AdmisionEmergencia(BaseModel):
    cedula: str
    nombre_completo: str
    numero_seguro: str
    hospital_id: str
    tipo_emergencia: str
    sintomas: str
    operador_id: str

@app.post("/")
async def admision_emergencia_handler(payload: AdmisionEmergencia):
    """Endpoint específico para admisión de emergencia - Reto 4"""
    try:
        # Generar ID único de admisión
        admission_id = f"ADM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # 1. Validar póliza con Gemini Pro
        policy_validation = await _validate_policy_async(payload)
        
        # 2. Revisar historial de preexistencias
        preexistencias = await _check_preexisting_conditions_async(payload.cedula)
        
        # 3. Generar respuestas secuenciales para chat
        chat_responses = [
            {
                "step": "validacion_poliza",
                "message": "Validando póliza...",
                "delay": 0
            },
            {
                "step": "validacion_poliza_result",
                "message": policy_validation.get("message", "Póliza validada automáticamente"),
                "delay": 1500
            },
            {
                "step": "revision_preexistencias",
                "message": f"Revisando historial de preexistencias para paciente [{payload.nombre_completo}]...",
                "delay": 1500
            },
            {
                "step": "revision_preexistencias_result",
                "message": preexistencias.get("message", "No se encontraron atenciones previas en el historial."),
                "delay": 1500
            }
        ]
        
        # 4. Enviar notificaciones simultáneas
        notifications = await _send_simultaneous_notifications(payload, admission_id)
        
        # 5. Guardar registro de admisión
        admission_record = {
            "admission_id": admission_id,
            "cedula": payload.cedula,
            "nombre_completo": payload.nombre_completo,
            "numero_seguro": payload.numero_seguro,
            "hospital_id": payload.hospital_id,
            "tipo_emergencia": payload.tipo_emergencia,
            "sintomas": payload.sintomas,
            "operador_id": payload.operador_id,
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "policy_validation": policy_validation,
            "preexistencias": preexistencias,
            "notifications": notifications
        }
        
        db.collection("admissions").add(admission_record)
        
        return {
            "status": "success",
            "admission_id": admission_id,
            "timestamp": datetime.now().isoformat(),
            "estimated_duration": "15 segundos",
            "chat_responses": chat_responses,
            "notifications": notifications,
            "message": "✅ Admisión de emergencia procesada correctamente - Reto 4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel serverless function handler
handler = app
