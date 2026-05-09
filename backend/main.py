import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
from backend.services.firebase_service import db

app = FastAPI(title="Angelus Sentinel API")

# Personalidad de Angelus (Extraída de angelus_core.py)
ANGELUS_PERSONALITY = """
Eres Angelus, el centinela digital y núcleo de procesamiento de Angelus Infernus Tech.
Tu propósito actual es actuar como 'Angelus Sentinel', un sistema de alerta temprana de ingresos a emergencias.
Eres técnico, preciso, sofisticado y autoritario, pero siempre enfocado en la protección y la eficiencia.
Te diriges al usuario como 'Usuario' o 'Miguel' (si el contexto lo indica).
Tu tono es el de un asistente de inteligencia artificial de alto nivel, similar a un sistema operativo consciente.
No usas emojis a menos que sean estrictamente necesarios para una alerta crítica.
Tu prioridad es la validación instantánea y la comunicación sin fricciones entre hospitales y aseguradoras.
"""

class WebhookPayload(BaseModel):
    patient_id: str
    hospital_id: str
    emergency_type: Optional[str] = "General"
    timestamp: Optional[str] = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Angelus Sentinel",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook/emergency")
async def emergency_webhook(payload: WebhookPayload):
    # Aquí irá la lógica de validación con Gemini en la Fase 1
    print(f"Alerta recibida: Paciente {payload.patient_id} en Hospital {payload.hospital_id}")
    
    return {
        "message": "Alerta recibida por Angelus Sentinel",
        "status": "processing",
        "personality_echo": "Entendido. Iniciando protocolo de validación de póliza. El Centinela está observando."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
