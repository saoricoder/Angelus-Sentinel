"""
Script para verificar la conexión a Firebase y revisar las bases de datos existentes
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def test_firebase_connection():
    """Prueba la conexión a Firebase con las credenciales proporcionadas"""
    
    print("🔍 Verificando conexión a Firebase...")
    
    # Configuración de Firebase desde las credenciales proporcionadas
    firebase_config = {
        "type": "service_account",
        "project_id": "angelusinfernustecnology",
        "private_key_id": "0e3765040524489ba0abb80c954e41886396b3eb",
        "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQxe9Nf9EhhEAR
/4odbl3vy7oY6nltrhxsmFn90dvlZ5Z5Cby3joOE6p8UVD180G6jNiAwYyH/ktLI
KYR/gy5Cb8BBVE2AcnkKqUG5qghQu8bxcg+eIs+Z4SUk5dPlh++d15TwdbRcP0M8
JBVaKGU5wyTP7oMgMRdtuKSv3vrCBODsHNA2pVz6+sf3lczxH6rHJ53ic0bqujcS
STSR0oIVLd8Touui7zPGLEkd66CVKx1y2sXzPCR7nvV2BIZSsT0aHM6OdC/l8HUM
zH2na6xA7ThmRROtbtv6H6QCbNzOWopI8h2ErrCKZAZ+Qa0Ol4DrihDQ6QBW1w1k
7DGkZ5+bAgMBAAECggEAO2ZdwHCh+YXNzvEkhFwvCPevksA/3VeBCdrNG/0WMi6n
bve4xIcdX3d73IZdWkJZgEF5phrGhRdqtn2tj7QsuMVf75aDWIz5aHGg3CkHJaVP
pMm9rNIdvBwFe/qSMAfdwsygOUxcDTUItbdUherhZi5iLnEfyMx+7H5xCQMJ2KKU
G9Sg/wYTKHFOP2qkuLjF33UARcCgqNdK71Y50aEVj9+w2Qs1RTLMQChOrUo8LthN
w/4NSJjiMzMTxTzV/0E0AN9Jw+WVrKqFtIzVKY9CDRMdduzcON1pQtinQhvkXL8M
b3OvTTNNBsYM5oUVgXgZsoyP1eZb43eE1M904ha5OQKBgQDtlw1rPEkZT4fXy24g
GpzBw3oGDd1Xh+YL7oVm8aiONnTJZ2HDWXHI2CCXIYKGgGhYRnQNoAQvuLtDOtVn
k1xXGIo+68FafKwvZoE9QRXtsITqvBO30BrxDv4lWzKPSLMlaRqgr7I9mvdojqwZ
o/wjHcC8fvZPQV9zXjwen/1OWQKBgQDg80Hrg62WFdtkwA9teRk4350KG60qfYaU
2+eJuTGCA9fSNGtNK+/iid7RKdkoyKyaYC7hQaLakmT2kETQ1VmzOlvnUGNAd6iy
CjwLLGYu+ToatytSp/X89/8GvxK6oeHWHncpIIr9CRG4jkB9QcSningRfL7xVqlD
PWa3ih1nEwKBgGDf8GbDJAMf/IGuvu50K2qOK9kAGjowfUpsLRS2gEXMSn48mw4u
EEkWZuN4lGIHRYSI5ZUQo+RZbHGTMaST31jb9rKFKkedAhApuZSiTzClguy7V0bh
obqcpF/S+aCWwgUFAAh42zJnV23Yjq+9v3cKEKZLFl9mhmbiC51pGr2xAoGAIUU5
QbkXCnSvH0acwYdAqL3B/0W6pecs6YVgyGjgnqcs24UvPZm7ABl+IBd9a9/KT4bc
SCqqCIPQdPs/glebzbta7mpgU5+fDr4exVRKxLXN1zeyK6Z15nVTfc7y2TGqMj4N
R8Lta6FUwqQfe6cni9QaEBQQNaeony5Mq+a8lIsCgYEAhn+iPFHdAr/TF8RMh1Ih
JRKbXLMCCxiHjol461R0Sax3MEDoQX2NAuPjUHLYxns/vEm2FhXBMpaGrysUCGSX
bAdXFlkKlryrnH8SonZWcdgFltGuPN0QrWv7MzetcFS/lp4Dp0XVENKlFh3gYvXO
EzV5GFj6UZAn0tNGtfx9u7o=\n-----END PRIVATE KEY-----""",
        "client_email": "firebase-adminsdk-fbsvc@angelusinfernustecnology.iam.gserviceaccount.com",
        "client_id": "103353548335447661941",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40angelusinfernustecnology.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    try:
        # Inicializar Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            firebase_app = firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente")
        else:
            firebase_app = firebase_admin.get_app()
            print("✅ Firebase ya estaba inicializado")
        
        # Conectar a la base de datos
        db = firestore.client()
        print("✅ Conexión a Firestore establecida")
        
        return db
        
    except Exception as e:
        print(f"❌ Error al conectar a Firebase: {e}")
        return None

def check_database_collections(db):
    """Revisa las colecciones existentes en la base de datos"""
    
    print("\n📋 Revisando colecciones en la base de datos...")
    
    if not db:
        print("❌ No hay conexión a la base de datos")
        return
    
    try:
        # Listar todas las colecciones
        collections = db.collections()
        
        collection_names = []
        for collection in collections:
            collection_names.append(collection.id)
        
        print(f"📊 Colecciones encontradas: {len(collection_names)}")
        for name in sorted(collection_names):
            print(f"  - {name}")
        
        # Colecciones esperadas según el código
        expected_collections = [
            "db_hospital_publico", "db_hospital_privado", "db_clinica", 
            "db_seguro_iess", "db_seguro_privado", "db_salud_publica",
            "patients", "notifications", "hospital_notifications", 
            "insurance_logs", "admissions"
        ]
        
        print(f"\n🎯 Colecciones esperadas por el sistema: {len(expected_collections)}")
        for expected in expected_collections:
            status = "✅" if expected in collection_names else "❌"
            print(f"  {status} {expected}")
        
        return collection_names
        
    except Exception as e:
        print(f"❌ Error al listar colecciones: {e}")
        return []

def check_collection_data(db, collection_name, limit=5):
    """Revisa los datos de una colección específica"""
    
    print(f"\n📄 Revisando datos en colección: {collection_name}")
    
    if not db:
        print("❌ No hay conexión a la base de datos")
        return
    
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.limit(limit).stream()
        
        doc_count = 0
        for doc in docs:
            doc_count += 1
            data = doc.to_dict()
            print(f"  📄 Documento {doc_count}: {doc.id}")
            print(f"     Datos: {json.dumps(data, indent=6, ensure_ascii=False)}")
            
            if doc_count >= limit:
                print(f"  ... (mostrando primeros {limit} documentos)")
                break
        
        if doc_count == 0:
            print(f"  ❌ La colección '{collection_name}' está vacía")
        else:
            print(f"  ✅ Se encontraron {doc_count} documentos")
            
    except Exception as e:
        print(f"❌ Error al leer colección '{collection_name}': {e}")

def main():
    """Función principal para verificar Firebase"""
    
    print("🚀 Iniciando verificación de Firebase para Angelus Sentinel")
    print("=" * 60)
    
    # 1. Probar conexión
    db = test_firebase_connection()
    
    if not db:
        print("\n❌ No se pudo establecer conexión a Firebase")
        return
    
    # 2. Listar colecciones
    collections = check_database_collections(db)
    
    # 3. Revisar datos en colecciones importantes
    important_collections = [
        "patients", "notifications", "hospital_notifications", 
        "insurance_logs", "admissions", "db_hospital_publico"
    ]
    
    for collection in important_collections:
        if collection in collections:
            check_collection_data(db, collection, limit=3)
        else:
            print(f"\n❌ Colección '{collection}' no existe")
    
    print("\n" + "=" * 60)
    print("🎯 Verificación completada")

if __name__ == "__main__":
    main()
