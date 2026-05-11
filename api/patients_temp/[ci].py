import json
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Import Firebase configuration
try:
    from backend.services.firebase_service import db
    from firebase_admin import firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    db = None

def handler(request):
    """Vercel serverless function for patients by CI - Reto 4"""
    
    # Extract CI from URL path
    path_parts = request.path.split('/')
    ci = path_parts[-1] if len(path_parts) > 1 else ''
    
    try:
        if not ci or len(ci) != 10:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({"error": "Invalid CI format"})
            }
        
        # Try to get patient from Firebase
        if FIREBASE_AVAILABLE and db:
            try:
                patients_ref = db.collection("patients")
                query = patients_ref.where("cedula", "==", ci).limit(1)
                docs = query.stream()
                
                patient_data = None
                for doc in docs:
                    patient_data = doc.to_dict()
                    break
                
                if patient_data:
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                        },
                        'body': json.dumps(patient_data)
                    }
            except Exception as firebase_error:
                print(f"Firebase error: {firebase_error}")
                # Fall back to test data if Firebase fails
        
        # Fallback to test patients database
        test_patients = {
            '1726354910': { 
                'nombre': 'Juan Pérez', 
                'numero_seguro': 'SEG-987654',
                'apellido': 'Pérez',
                'edad': 35,
                'tipo_sangre': 'O+',
                'cedula': '1726354910'
            },
            '0912345678': { 
                'nombre': 'María García', 
                'numero_seguro': 'SEG-123456',
                'apellido': 'García',
                'edad': 28,
                'tipo_sangre': 'A+',
                'cedula': '0912345678'
            },
            '1711223344': { 
                'nombre': 'Carlos Rodríguez', 
                'numero_seguro': 'SEG-555666',
                'apellido': 'Rodríguez',
                'edad': 42,
                'tipo_sangre': 'B+',
                'cedula': '1711223344'
            }
        }
        
        if ci in test_patients:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps(test_patients[ci])
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({"error": "Patient not found"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({"error": str(e)})
        }

app = handler
