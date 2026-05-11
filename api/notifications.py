import json

def handler(request):
    """Vercel serverless function for notifications history - Reto 4"""
    
    # Simple mock data
    notifications = [
        {
            "id": "hosp_001",
            "timestamp": "2025-05-11T14:07:00.000Z",
            "cedula": "1726354910",
            "target": "Departamento de Urgencias (Hospital)",
            "message": "Alerta Clinica: Paciente Juan Pérez (1726354910) ingresado con triage HIGH.",
            "type": "HOSPITAL",
            "status": "COMPLETADO"
        },
        {
            "id": "ins_001",
            "timestamp": "2025-05-11T14:07:00.000Z",
            "cedula": "1726354910",
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": "Validacion de Cobertura: Paciente Juan Pérez (1726354910). Estado de autorizacion: APPROVED.",
            "type": "INSURANCE",
            "status": "COMPLETADO"
        }
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(notifications)
    }

app = handler
