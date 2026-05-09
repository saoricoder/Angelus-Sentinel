import google.generativeai as genai
from backend.config import GEMINI_API_KEY, ANGELUS_PROMPT

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY no configurado en .env")

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_emergency_entry(self, patient_data: dict, policy_data: dict):
        """
        Analiza el ingreso de emergencia usando la personalidad de Angelus.
        """
        prompt = f"""
        {ANGELUS_PROMPT}
        
        CASO DE EMERGENCIA:
        Datos del Paciente: {patient_data}
        Datos de la Póliza: {policy_data}
        
        INSTRUCCIÓN:
        Analiza si el paciente tiene cobertura para este ingreso. 
        Detecta posibles preexistencias conflictivas.
        Genera una respuesta en formato JSON con los campos:
        - decision: "APROBADO" | "REVISIÓN MANUAL" | "RECHAZADO"
        - reasoning: "Breve explicación técnica"
        - angelus_reply: "Mensaje con tu personalidad para el gestor"
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error en la validación del Centinela: {str(e)}"

gemini_service = GeminiService()
