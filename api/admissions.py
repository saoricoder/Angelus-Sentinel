import json
from datetime import datetime

def handler(request):
    """Vercel serverless function for admissions - Reto 4"""
    
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
        # Parse request body
        body = json.loads(request.body)
        
        # Generate admission response (Reto 4)
        admission_id = f"ADM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # Simulate successful admission with notifications
        response_data = {
            "status": "success",
            "admission_id": admission_id,
            "timestamp": timestamp,
            "estimated_duration": "15 segundos",
            "chat_responses": [
                {
                    "step": "validacion_poliza",
                    "message": "Validando póliza...",
                    "delay": 0
                },
                {
                    "step": "validacion_poliza_result",
                    "message": "Éxito: Póliza validada automáticamente",
                    "delay": 1500
                },
                {
                    "step": "revision_preexistencias",
                    "message": f"Revisando historial de preexistencias para paciente [{body.get('nombre_completo', 'N/A')}]...",
                    "delay": 1500
                },
                {
                    "step": "revision_preexistencias_result",
                    "message": "No se encontraron atenciones previas en el historial.",
                    "delay": 1500
                }
            ],
            "notifications": {
                "hospital": {
                    "status": "delivered", 
                    "timestamp": timestamp,
                    "message": f"Notificación enviada a Departamento de Urgencias para {body.get('nombre_completo', 'N/A')}"
                },
                "insurance": {
                    "status": "delivered", 
                    "timestamp": timestamp,
                    "message": f"Notificación enviada a Gestor de Autorizaciones para {body.get('nombre_completo', 'N/A')}"
                },
                "execution": "simultaneous_parallel"
            },
            "message": "✅ Admisión de emergencia procesada correctamente - Reto 4"
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(response_data)
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
                "message": "Error procesando admisión de emergencia"
            })
        }

# Vercel expects 'app' or 'handler'
app = handler
