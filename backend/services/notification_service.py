import json
from datetime import datetime

class NotificationService:
    def __init__(self):
        # Aquí se podrían configurar webhooks reales de Discord, Slack, etc.
        self.logs = []

    async def notify_all(self, alert_data: dict):
        """
        Simula el envío de notificaciones simultáneas al hospital y a la aseguradora.
        """
        timestamp = datetime.now().isoformat()
        decision = alert_data.get('analysis', {}).get('decision', 'REVISIÓN')
        patient = alert_data.get('patient_name', 'Paciente')

        # Notificación 1: Hospital
        hosp_notif = {
            "timestamp": timestamp,
            "target": "Departamento de Admisiones (Hospital)",
            "message": f"Ingreso validado: {patient}. Estado: {decision}.",
            "type": "HOSPITAL",
            "status": "COMPLETADO"
        }
        
        # Notificación 2: Aseguradora
        insu_notif = {
            "timestamp": timestamp,
            "target": "Gestor de Casos (Aseguradora)",
            "message": f"Alerta de siniestro: {patient}. Análisis de IA completado.",
            "type": "INSURANCE",
            "status": "COMPLETADO"
        }

        self.logs.insert(0, hosp_notif)
        self.logs.insert(0, insu_notif)
        
        print(f"📡 [SIMULTÁNEO] Notificaciones enviadas para {patient}")
        return [hosp_notif, insu_notif]

notification_service = NotificationService()
