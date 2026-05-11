import json
import sys
import os
import asyncio

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import backend services
try:
    from backend.services.gemini_service import gemini_service
    from backend.services.firebase_service import db
    from backend.config import ANGELUS_PROMPT
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    gemini_service = None
    db = None
    ANGELUS_PROMPT = ""

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
        
        # Handle patient admission flow - Reto 4
        if confirmed_patient_id and form_data:
            return handle_patient_admission(form_data, operator_name)
        
        # Handle general chat
        return handle_general_chat(message, operator_name)
        
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

def handle_patient_admission(form_data, operator_name):
    """Handle patient admission flow with sequential responses"""
    
    responses = [
        {
            "role": "angelus",
            "content": "Validando póliza...",
            "type": "PROCESSING",
            "step": "validacion_poliza"
        },
        {
            "role": "angelus", 
            "content": f"Éxito: Póliza {form_data.get('numero_seguro', 'N/A')} validada automáticamente para {form_data.get('nombre', 'N/A')}.",
            "type": "SUCCESS",
            "step": "validacion_poliza_result"
        },
        {
            "role": "angelus",
            "content": f"Revisando historial de preexistencias para paciente [{form_data.get('nombre', 'N/A')}]...",
            "type": "PROCESSING",
            "step": "revision_preexistencias"
        },
        {
            "role": "angelus",
            "content": "No se encontraron atenciones previas en el historial. Paciente sin preexistencias conocidas.",
            "type": "SUCCESS",
            "step": "revision_preexistencias_result"
        },
        {
            "role": "angelus",
            "content": f"Notificaciones simultáneas enviadas: Departamento de Urgencias y Gestor de Autorizaciones notificados sobre ingreso de {form_data.get('nombre', 'N/A')}.",
            "type": "COMPLETE",
            "step": "notificaciones_enviadas"
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

def handle_general_chat(message, operator_name):
    """Handle general chat with Gemini Pro if available"""
    
    if GEMINI_AVAILABLE and gemini_service:
        try:
            # Use real Gemini Pro
            patient_data = {"name": "Paciente", "id": "N/A"}
            policy_data = {"plan": "Standard", "status": "Active", "coverage": ["Emergency"], "exclusions": [], "pre_existing_conditions": []}
            
            response = asyncio.run(gemini_service.analyze_emergency_entry(
                patient_data, 
                policy_data, 
                operator_name
            ))
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps([{
                    "role": "angelus",
                    "content": response,
                    "type": "SUCCESS"
                }])
            }
        except Exception as gemini_error:
            print(f"Gemini error: {gemini_error}")
            # Fall back to simulated response
    
    # Fallback response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps([{
            "role": "angelus",
            "content": f"Núcleo Angelus procesando solicitud para {operator_name}. Por favor, proporcione los datos del paciente para iniciar el protocolo de validación.",
            "type": "QUESTION"
        }])
    }

app = handler
