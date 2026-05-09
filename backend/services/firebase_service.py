import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from backend.config import load_dotenv

# Asegurar que las variables de entorno estén cargadas
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

firebase_app = None
db = None

def initialize_firebase():
    global firebase_app, db
    
    if not firebase_admin._apps:
        # Intentar cargar desde variable de entorno (JSON string)
        service_account_info = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        
        try:
            if service_account_info:
                # Parsear el string JSON
                info = json.loads(service_account_info)
                cred = credentials.Certificate(info)
            else:
                # Fallback a archivo físico si existe
                cred_path = os.path.join(os.path.dirname(__file__), "..", "..", "serviceAccountKey.json")
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                else:
                    print("ERROR: No se encontró configuración de Firebase (JSON o archivo)")
                    return None
            
            firebase_app = firebase_admin.initialize_app(cred)
            db = firestore.client(database_id="sentinel")
            print("Firebase inicializado correctamente en la base de datos 'sentinel'")
        except Exception as e:
            print(f"Error al inicializar Firebase: {e}")
            return None
    else:
        db = firestore.client(database_id="sentinel")
    
    return db

# Inicializar al importar si es posible
db = initialize_firebase()
