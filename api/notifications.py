import json
from datetime import datetime, timedelta

def handler(request):
    """Vercel serverless function for notifications history - Reto 4"""
    
    try:
        # Generate mock notifications data for testing
        mock_notifications = generate_mock_notifications()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(mock_notifications)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps([{
                "error": str(e),
                "message": "Error obteniendo notificaciones"
            }])
        }

def generate_mock_notifications():
    """Generate mock notifications data for testing"""
    
    now = datetime.now()
    notifications = []
    
    # Hospital notifications
    hospital_notifications = [
        {
            "id": "hosp_001",
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "cedula": "1726354910",
            "target": "Departamento de Urgencias (Hospital)",
            "message": "Alerta Clinica: Paciente Juan Pérez (1726354910) ingresado con triage HIGH.",
            "type": "HOSPITAL",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": "Juan Pérez",
                "ci": "1726354910",
                "triage_priority": "HIGH",
                "symptoms": "Paciente en admisión de emergencia",
                "clinical_history": [],
                "ai_recommendation": "Paciente estable para observacion"
            }
        },
        {
            "id": "hosp_002", 
            "timestamp": (now - timedelta(minutes=15)).isoformat(),
            "cedula": "0912345678",
            "target": "Departamento de Urgencias (Hospital)",
            "message": "Alerta Clinica: Paciente María García (0912345678) ingresado con triage MEDIUM.",
            "type": "HOSPITAL",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": "María García",
                "ci": "0912345678",
                "triage_priority": "MEDIUM",
                "symptoms": "Dolor abdominal agudo",
                "clinical_history": ["Apendicectomía 2020"],
                "ai_recommendation": "Evaluar cirugía de emergencia"
            }
        }
    ]
    
    # Insurance notifications
    insurance_notifications = [
        {
            "id": "ins_001",
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "cedula": "1726354910",
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": "Validacion de Cobertura: Paciente Juan Pérez (1726354910). Estado de autorizacion: APPROVED.",
            "type": "INSURANCE",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": "Juan Pérez",
                "ci": "1726354910",
                "insurance_status": {"policy": "SEG-987654", "status": "ACTIVE"},
                "triage_priority": "HIGH",
                "decision": "APPROVED"
            }
        },
        {
            "id": "ins_002",
            "timestamp": (now - timedelta(minutes=15)).isoformat(),
            "cedula": "0912345678",
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": "Validacion de Cobertura: Paciente María García (0912345678). Estado de autorizacion: APPROVED.",
            "type": "INSURANCE",
            "status": "COMPLETADO",
            "payload": {
                "patient_name": "María García",
                "ci": "0912345678",
                "insurance_status": {"policy": "SEG-123456", "status": "ACTIVE"},
                "triage_priority": "MEDIUM",
                "decision": "APPROVED"
            }
        }
    ]
    
    # Combine and sort by timestamp
    all_notifications = hospital_notifications + insurance_notifications
    all_notifications.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return all_notifications

app = handler
