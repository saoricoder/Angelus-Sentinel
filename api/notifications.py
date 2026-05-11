import json

def handler(request):
    """Vercel serverless function for notifications history - Reto 4"""
    
    notifications = [
        {
            "id": "hosp_001",
            "timestamp": "2025-05-11T14:07:00.000Z",
            "cedula": "1726354910",
            "target": "Departamento de Urgencias (Hospital)",
            "message": "Alerta Clinica: Paciente Juan Perez (1726354910) ingresado con triage HIGH.",
            "type": "HOSPITAL",
            "status": "COMPLETADO"
        },
        {
            "id": "ins_001",
            "timestamp": "2025-05-11T14:07:00.000Z",
            "cedula": "1726354910",
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": "Validacion de Cobertura: Paciente Juan Perez (1726354910). Estado de autorizacion: APPROVED.",
            "type": "INSURANCE",
            "status": "COMPLETADO"
        }
    ]
    
    return json.dumps(notifications)

app = handler
