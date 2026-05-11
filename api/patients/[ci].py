import json

def handler(request):
    """Vercel serverless function for patients by CI - Reto 4"""
    
    # Extract CI from URL path
    path_parts = request.path.split('/')
    ci = path_parts[-1] if len(path_parts) > 1 else ''
    
    try:
        # Test patients database (simulated)
        test_patients = {
            '1726354910': { 
                'nombre': 'Juan Pérez', 
                'numero_seguro': 'SEG-987654',
                'apellido': 'Pérez',
                'edad': 35,
                'tipo_sangre': 'O+'
            },
            '0912345678': { 
                'nombre': 'María García', 
                'numero_seguro': 'SEG-123456',
                'apellido': 'García',
                'edad': 28,
                'tipo_sangre': 'A+'
            },
            '1711223344': { 
                'nombre': 'Carlos Rodríguez', 
                'numero_seguro': 'SEG-555666',
                'apellido': 'Rodríguez',
                'edad': 42,
                'tipo_sangre': 'B+'
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
