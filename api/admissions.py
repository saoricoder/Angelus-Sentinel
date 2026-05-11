import json
import os
from datetime import datetime

def handler(request):
    """Vercel serverless function for emergency admissions - Reto 4"""
    
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
        
        # Validate required fields
        required_fields = ['cedula', 'nombre_completo', 'numero_seguro', 'hospital_id', 'tipo_emergencia', 'sintomas', 'operador_id']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    'body': json.dumps({"error": f"Missing required field: {field}"})
                }
        
        # Generate unique admission ID
        admission_id = f"ADM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # Simulate policy validation
        policy_validation = {
            "status": "APPROVED",
            "message": "Póliza validada correctamente",
            "policy_number": body['numero_seguro'],
            "coverage_level": "PREMIUM"
        }
        
        # Simulate pre-existing conditions check
        preexistencias = {
            "status": "FOUND",
            "message": f"Se encontraron condiciones preexistentes para paciente {body['nombre_completo']}",
            "conditions": ["Hipertensión"],
            "impact": "CONTROLLED"
        }
        
        # Generate sequential chat responses
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
                "message": f"Revisando historial de preexistencias para paciente [{body['nombre_completo']}]...",
                "delay": 1500
            },
            {
                "step": "revision_preexistencias_result",
                "message": preexistencias.get("message", "No se encontraron atenciones previas en el historial."),
                "delay": 1500
            }
        ]
        
        # Simulate simultaneous notifications
        notifications = {
            "hospital": {"status": "delivered", "timestamp": timestamp},
            "insurance": {"status": "delivered", "timestamp": timestamp},
            "execution": "simultaneous_parallel"
        }
        
        # Create admission record
        admission_record = {
            "admission_id": admission_id,
            "cedula": body['cedula'],
            "nombre_completo": body['nombre_completo'],
            "numero_seguro": body['numero_seguro'],
            "hospital_id": body['hospital_id'],
            "tipo_emergencia": body['tipo_emergencia'],
            "sintomas": body['sintomas'],
            "operador_id": body['operador_id'],
            "timestamp": timestamp,
            "status": "completed",
            "policy_validation": policy_validation,
            "preexistencias": preexistencias,
            "notifications": notifications
        }
        
        # Try to save to Firebase (if available)
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Try to initialize Firebase with environment variable
            service_account_info = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            if service_account_info:
                info = json.loads(service_account_info)
                cred = credentials.Certificate(info)
                
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred)
                
                db = firestore.client()
                db.collection("admissions").add(admission_record)
                print("✅ Admission saved to Firebase")
        except Exception as firebase_error:
            print(f"⚠️ Firebase not available: {firebase_error}")
            # Continue without Firebase
        
        return {
            "status": "success",
            "admission_id": admission_id,
            "timestamp": timestamp,
            "estimated_duration": "15 segundos",
            "chat_responses": chat_responses,
            "notifications": notifications,
            "message": "✅ Admisión de emergencia procesada correctamente - Reto 4"
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

app = handler
