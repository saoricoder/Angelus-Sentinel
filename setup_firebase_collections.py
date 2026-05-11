"""
Script para crear las colecciones faltantes en Firebase para Angelus Sentinel - Reto 4
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

def setup_firebase_collections():
    """Crea las colecciones necesarias para Angelus Sentinel"""
    
    print("🔧 Configurando colecciones de Firebase para Angelus Sentinel...")
    
    # Configuración de Firebase
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
        
        db = firestore.client()
        print("✅ Conexión a Firestore establecida")
        
        return db
        
    except Exception as e:
        print(f"❌ Error al conectar a Firebase: {e}")
        return None

def create_hospital_databases(db):
    """Crea las 6 bases de datos simuladas de hospitales y seguros"""
    
    print("\n🏥 Creando bases de datos de hospitales y seguros...")
    
    # Datos de prueba para las 6 bases de datos
    databases_data = {
        "db_hospital_publico": [
            {
                "id": "1726354910",
                "name": "Juan Pérez",
                "age": 35,
                "blood_type": "O+",
                "admissions": [
                    {
                        "date": "2024-03-15",
                        "diagnosis": "Apendicitis aguda",
                        "treatment": "Apendicectomía",
                        "status": "completed"
                    }
                ],
                "allergies": ["Penicilina"],
                "chronic_conditions": ["Hipertensión"],
                "last_visit": "2024-10-20"
            },
            {
                "id": "0912345678",
                "name": "María García",
                "age": 42,
                "blood_type": "A+",
                "admissions": [
                    {
                        "date": "2024-01-10",
                        "diagnosis": "Neumonía",
                        "treatment": "Antibióticos",
                        "status": "completed"
                    }
                ],
                "allergies": [],
                "chronic_conditions": ["Diabetes tipo 2"],
                "last_visit": "2024-11-15"
            }
        ],
        
        "db_hospital_privado": [
            {
                "id": "1711223344",
                "name": "Carlos Rodríguez",
                "age": 28,
                "blood_type": "B+",
                "admissions": [
                    {
                        "date": "2024-06-22",
                        "diagnosis": "Fractura de muñeca",
                        "treatment": "Yeso y rehabilitación",
                        "status": "completed"
                    }
                ],
                "allergies": ["Ibuprofeno"],
                "chronic_conditions": [],
                "last_visit": "2024-09-10"
            }
        ],
        
        "db_clinica": [
            {
                "id": "1726354910",
                "name": "Juan Pérez",
                "age": 35,
                "blood_type": "O+",
                "consultations": [
                    {
                        "date": "2024-08-05",
                        "reason": "Control postoperatorio",
                        "diagnosis": "Recuperación normal",
                        "status": "completed"
                    }
                ],
                "medications": ["Losartán", "Omeprazol"],
                "last_visit": "2024-11-01"
            }
        ],
        
        "db_seguro_iess": [
            {
                "id": "1726354910",
                "name": "Juan Pérez",
                "policy_number": "IESS-001",
                "coverage_level": "Completo",
                "valid_until": "2025-12-31",
                "preexisting_conditions": ["Hipertensión"],
                "deductible": 0,
                "copayment": 5.0
            },
            {
                "id": "0912345678",
                "name": "María García",
                "policy_number": "IESS-002",
                "coverage_level": "Básico",
                "valid_until": "2025-06-30",
                "preexisting_conditions": ["Diabetes tipo 2"],
                "deductible": 50.0,
                "copayment": 10.0
            }
        ],
        
        "db_seguro_privado": [
            {
                "id": "1711223344",
                "name": "Carlos Rodríguez",
                "policy_number": "PRIV-001",
                "coverage_level": "Premium",
                "valid_until": "2026-03-31",
                "preexisting_conditions": [],
                "deductible": 0,
                "copayment": 0.0,
                "additional_benefits": ["Dental", "Visual", " Internacional"]
            }
        ],
        
        "db_salud_publica": [
            {
                "id": "1726354910",
                "name": "Juan Pérez",
                "registration_date": "2020-01-15",
                "health_center": "Centro de Salud Norte",
                "vaccinations": ["COVID-19", "Influenza", "Hepatitis B"],
                "conditions": ["Hipertensión"],
                "last_checkup": "2024-10-15"
            },
            {
                "id": "0912345678",
                "name": "María García",
                "registration_date": "2019-05-20",
                "health_center": "Centro de Salud Sur",
                "vaccinations": ["COVID-19", "Tétanos"],
                "conditions": ["Diabetes tipo 2"],
                "last_checkup": "2024-11-10"
            }
        ]
    }
    
    for db_name, patients in databases_data.items():
        print(f"  📝 Creando {db_name}...")
        try:
            for patient in patients:
                doc_ref = db.collection(db_name).document(patient["id"])
                doc_ref.set(patient)
            print(f"    ✅ {db_name} creada con {len(patients)} pacientes")
        except Exception as e:
            print(f"    ❌ Error creando {db_name}: {e}")

def create_angelus_collections(db):
    """Crea las colecciones específicas de Angelus Sentinel"""
    
    print("\n🏥 Creando colecciones de Angelus Sentinel...")
    
    # Colección notifications
    notifications_data = [
        {
            "id": "notif_001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cedula": "1726354910",
            "target": "Departamento de Urgencias (Hospital)",
            "message": "Alerta Clínica: Paciente Juan Pérez (1726354910) ingresado con triage HIGH.",
            "type": "HOSPITAL",
            "status": "COMPLETADO",
            "priority": "HIGH"
        },
        {
            "id": "notif_002",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cedula": "1726354910",
            "target": "Gestor de Autorizaciones (Aseguradora)",
            "message": "Validación de Cobertura: Paciente Juan Pérez (1726354910). Estado de autorización: APPROVED.",
            "type": "INSURANCE",
            "status": "COMPLETADO",
            "priority": "MEDIUM"
        }
    ]
    
    print("  📝 Creando notifications...")
    for notif in notifications_data:
        doc_ref = db.collection("notifications").document(notif["id"])
        doc_ref.set(notif)
    print(f"    ✅ notifications creada con {len(notifications_data)} notificaciones")
    
    # Colección hospital_notifications
    hospital_notifications_data = [
        {
            "id": "hosp_notif_001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "patient_id": "1726354910",
            "patient_name": "Juan Pérez",
            "hospital_id": "HOSP-METROPOLITANO",
            "department": "Urgencias",
            "message": "Paciente admitido en urgencias - Prioridad ALTA",
            "triage_level": "HIGH",
            "status": "ACTIVE"
        }
    ]
    
    print("  📝 Creando hospital_notifications...")
    for notif in hospital_notifications_data:
        doc_ref = db.collection("hospital_notifications").document(notif["id"])
        doc_ref.set(notif)
    print(f"    ✅ hospital_notifications creada con {len(hospital_notifications_data)} notificaciones")
    
    # Colección insurance_logs
    insurance_logs_data = [
        {
            "id": "ins_log_001",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "patient_id": "1726354910",
            "policy_number": "IESS-001",
            "insurance_company": "IESS",
            "validation_result": "APPROVED",
            "coverage_details": {
                "emergency_coverage": "FULL",
                "deductible": 0,
                "copayment": 5.0
            },
            "preexisting_conditions": ["Hipertensión"],
            "status": "COMPLETED"
        }
    ]
    
    print("  📝 Creando insurance_logs...")
    for log in insurance_logs_data:
        doc_ref = db.collection("insurance_logs").document(log["id"])
        doc_ref.set(log)
    print(f"    ✅ insurance_logs creada con {len(insurance_logs_data)} logs")
    
    # Colección admissions
    admissions_data = [
        {
            "id": "ADM-20250511-143000",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cedula": "1726354910",
            "nombre_completo": "Juan Pérez",
            "numero_seguro": "IESS-001",
            "hospital_id": "HOSP-METROPOLITANO",
            "tipo_emergencia": "URGENCIA",
            "sintomas": "Dolor abdominal agudo",
            "operador_id": "OP001",
            "policy_validation": {
                "status": "APPROVED",
                "message": "Póliza validada correctamente",
                "coverage": "FULL"
            },
            "preexisting_conditions": {
                "status": "FOUND",
                "conditions": ["Hipertensión"],
                "impact": "CONTROLLED"
            },
            "notifications": {
                "hospital": {"status": "SENT", "timestamp": datetime.now(timezone.utc).isoformat()},
                "insurance": {"status": "SENT", "timestamp": datetime.now(timezone.utc).isoformat()}
            },
            "status": "COMPLETED"
        }
    ]
    
    print("  📝 Creando admissions...")
    for admission in admissions_data:
        doc_ref = db.collection("admissions").document(admission["id"])
        doc_ref.set(admission)
    print(f"    ✅ admissions creada con {len(admissions_data)} admisiones")

def main():
    """Función principal"""
    
    print("🚀 Configurando Firebase para Angelus Sentinel - Reto 4")
    print("=" * 60)
    
    # 1. Conectar a Firebase
    db = setup_firebase_collections()
    
    if not db:
        print("\n❌ No se pudo establecer conexión a Firebase")
        return
    
    # 2. Crear bases de datos de hospitales y seguros
    create_hospital_databases(db)
    
    # 3. Crear colecciones de Angelus Sentinel
    create_angelus_collections(db)
    
    print("\n" + "=" * 60)
    print("✅ Configuración completada exitosamente")
    print("🎯 Firebase está listo para Angelus Sentinel - Reto 4")

if __name__ == "__main__":
    main()
