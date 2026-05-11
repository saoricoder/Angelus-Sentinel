import json

def handler(request):
    """Vercel serverless function for chat with Angelus AI - Reto 4"""
    
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
        message = body.get('message', '')
        operator_name = body.get('operator_name', 'Operador')
        confirmed_patient_id = body.get('confirmed_patient_id', '')
        form_data = body.get('form_data', {})
        
        # Simulate Angelus AI responses
        if confirmed_patient_id and form_data:
            # Patient admission flow - Reto 4
            responses = [
                {
                    "role": "angelus",
                    "content": "Validando póliza...",
                    "type": "PROCESSING"
                },
                {
                    "role": "angelus", 
                    "content": f"Éxito: Póliza {form_data.get('numero_seguro', 'N/A')} validada automáticamente para {form_data.get('nombre', 'N/A')}.",
                    "type": "SUCCESS"
                },
                {
                    "role": "angelus",
                    "content": f"Revisando historial de preexistencias para paciente [{form_data.get('nombre', 'N/A')}]...",
                    "type": "PROCESSING"
                },
                {
                    "role": "angelus",
                    "content": "No se encontraron atenciones previas en el historial. Paciente sin preexistencias conocidas.",
                    "type": "SUCCESS"
                },
                {
                    "role": "angelus",
                    "content": f"Notificaciones simultáneas enviadas: Departamento de Urgencias y Gestor de Autorizaciones notificados sobre ingreso de {form_data.get('nombre', 'N/A')}.",
                    "type": "COMPLETE"
                }
            ]
        else:
            # General chat response
            responses = [
                {
                    "role": "angelus",
                    "content": f"Núcleo Angelus procesando solicitud para {operator_name}. Por favor, proporcione los datos del paciente para iniciar el protocolo de validación.",
                    "type": "QUESTION"
                }
            ]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(responses)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps([{
                "role": "angelus",
                "content": f"Error en el procesamiento: {str(e)}",
                "type": "ERROR"
            }])
        }

app = handler
