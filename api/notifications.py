import json

def handler(request):
    """Vercel serverless function for notifications - Reto 4"""
    
    try:
        # Simple response for notifications
        notifications = [
            {
                "timestamp": "2025-05-11T12:58:00.000Z",
                "target": "Departamento de Urgencias (Hospital)",
                "message": "Alerta Clinica: Paciente Juan Pérez (1726354910) ingresado con triage HIGH.",
                "type": "HOSPITAL",
                "status": "COMPLETADO"
            },
            {
                "timestamp": "2025-05-11T12:58:00.000Z",
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
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps([{"error": str(e)}])
        }

app = handler
