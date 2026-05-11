import json
from datetime import datetime

def handler(request):
    """Vercel serverless function for notifications - Reto 4"""
    
    # Handle CORS
    if request.method == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    try:
        # Simulate notification logs (Reto 4)
        notification_logs = [
            {
                "timestamp": datetime.now().isoformat(),
                "target": "Departamento de Urgencias (Hospital)",
                "message": "Alerta Clínica: Paciente Juan Pérez (1726354910) ingresado con triage HIGH.",
                "type": "HOSPITAL",
                "status": "COMPLETADO",
                "payload": {
                    "patient_name": "Juan Pérez",
                    "ci": "1726354910",
                    "triage_priority": "HIGH",
                    "symptoms": "Paciente en admisión de emergencia",
                    "clinical_history": [],
                    "ai_recommendation": "Paciente estable para observación"
                }
            },
            {
                "timestamp": datetime.now().isoformat(),
                "target": "Gestor de Autorizaciones (Aseguradora)",
                "message": "Validación de Cobertura: Paciente Juan Pérez (1726354910). Estado de autorización: APPROVED.",
                "type": "INSURANCE",
                "status": "COMPLETADO",
                "payload": {
                    "patient_name": "Juan Pérez",
                    "ci": "1726354910",
                    "insurance_status": {"policy": "SEG-987654", "status": "ACTIVE"},
                    "triage_priority": "HIGH",
                    "decision": "APPROVED"
                }
            }
        ]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(notification_logs)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                "error": str(e),
                "message": "Error obteniendo notificaciones"
            })
        }

# Vercel expects 'app' or 'handler'
app = handler
