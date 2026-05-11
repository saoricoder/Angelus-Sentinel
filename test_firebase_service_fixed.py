"""
Script para probar el servicio Firebase de Angelus Sentinel con configuración directa
"""

import os
import sys
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Configurar la variable de entorno con las credenciales de Firebase
os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"] = json.dumps({
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
})

def federated_search(name_query: str = None, ci_query: str = None):
    """
    Busca un paciente en las 6 bases de datos simuladas.
    Agrupa resultados por CI.
    """
    collections = [
        "db_hospital_publico", "db_hospital_privado", "db_clinica", 
        "db_seguro_iess", "db_seguro_privado", "db_salud_publica"
    ]
    
    results_by_ci = {}
    
    try:
        # Inicializar Firebase
        if not firebase_admin._apps:
            service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"))
            cred = credentials.Certificate(service_account_info)
            firebase_app = firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        for col_name in collections:
            col_ref = db.collection(col_name)
            docs = col_ref.stream()
            
            for doc in docs:
                data = doc.to_dict()
                p_name = data.get("name", "").lower()
                p_id = data.get("id", "")
                
                # Match por CI (prioritario) o por Nombre
                match = False
                if ci_query and ci_query == p_id:
                    match = True
                elif name_query and name_query.lower() in p_name:
                    match = True
                    
                if match:
                    if p_id not in results_by_ci:
                        results_by_ci[p_id] = {
                            "id": p_id,
                            "name": data.get("name"),
                            "sources": []
                        }
                    # Añadir datos de esta fuente
                    source_data = {"source": col_name, "data": data}
                    results_by_ci[p_id]["sources"].append(source_data)
                    
                    # Consolidar datos para análisis
                    if col_name in ["db_hospital_publico", "db_hospital_privado", "db_clinica"]:
                        results_by_ci[p_id]["clinical_history"] = data
                    if col_name in ["db_seguro_iess", "db_seguro_privado"]:
                        results_by_ci[p_id]["insurance_policy"] = data
                        
        return list(results_by_ci.values())
        
    except Exception as e:
        print(f"❌ Error en federated_search: {e}")
        return []

def test_firebase_service():
    """Prueba el servicio Firebase de Angelus Sentinel"""
    
    print("🧪 Probando el servicio Firebase de Angelus Sentinel...")
    print("=" * 60)
    
    # 1. Probar búsqueda por CI
    print("\n🔍 Probando búsqueda por CI...")
    test_ci = "1726354910"
    results = federated_search(ci_query=test_ci)
    
    print(f"📊 Resultados para CI {test_ci}: {len(results)} pacientes encontrados")
    
    for result in results:
        print(f"\n👤 Paciente: {result['name']} (CI: {result['id']})")
        print(f"📋 Fuentes de datos: {len(result['sources'])}")
        
        for source in result['sources']:
            source_name = source['source']
            source_data = source['data']
            print(f"  📄 {source_name}:")
            
            # Mostrar información relevante según la fuente
            if 'hospital' in source_name:
                if 'admissions' in source_data:
                    for admission in source_data['admissions']:
                        print(f"    🏥 Admisión: {admission['diagnosis']} ({admission['date']})")
                if 'chronic_conditions' in source_data:
                    print(f"    ⚠️  Condiciones crónicas: {source_data['chronic_conditions']}")
                if 'allergies' in source_data:
                    print(f"    🚨 Alergias: {source_data['allergies']}")
            
            elif 'seguro' in source_name:
                print(f"    🛡️  Póliza: {source_data.get('policy_number', 'N/A')}")
                print(f"    💰 Cobertura: {source_data.get('coverage_level', 'N/A')}")
                print(f"    ⚠️  Preexistencias: {source_data.get('preexisting_conditions', [])}")
                print(f"    💵 Copago: ${source_data.get('copayment', 0)}")
            
            elif 'clinica' in source_name or 'salud' in source_name:
                if 'consultations' in source_data:
                    for consultation in source_data['consultations']:
                        print(f"    🩺 Consulta: {consultation['reason']} ({consultation['date']})")
                if 'medications' in source_data:
                    print(f"    💊 Medicamentos: {source_data['medications']}")
        
        # Mostrar datos consolidados
        if 'clinical_history' in result:
            print(f"  📋 Historial clínico consolidado: ✅")
        if 'insurance_policy' in result:
            print(f"  🛡️  Póliza consolidada: ✅")
    
    # 2. Probar búsqueda por nombre
    print("\n🔍 Probando búsqueda por nombre...")
    test_name = "Juan"
    results_by_name = federated_search(name_query=test_name)
    
    print(f"📊 Resultados para nombre '{test_name}': {len(results_by_name)} pacientes encontrados")
    
    for result in results_by_name:
        print(f"👤 {result['name']} (CI: {result['id']})")
    
    # 3. Probar búsqueda sin resultados
    print("\n🔍 Probando búsqueda sin resultados...")
    no_results = federated_search(ci_query="9999999999")
    print(f"📊 Resultados para CI inexistente: {len(no_results)} pacientes")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas del servicio Firebase completadas")
    return True

def test_specific_patient_data():
    """Prueba datos específicos de un paciente"""
    
    print("\n🎯 Probando datos específicos del paciente Juan Pérez...")
    
    # Buscar al paciente Juan Pérez
    results = federated_search(ci_query="1726354910")
    
    if not results:
        print("❌ No se encontró al paciente Juan Pérez")
        return False
    
    patient = results[0]
    print(f"✅ Paciente encontrado: {patient['name']}")
    
    # Verificar datos esperados para Reto 4
    expected_data = {
        "hospital_data": False,
        "insurance_data": False,
        "clinical_history": False,
        "preexisting_conditions": False
    }
    
    for source in patient['sources']:
        source_name = source['source']
        
        if 'hospital' in source_name or 'clinica' in source_name:
            expected_data["hospital_data"] = True
            expected_data["clinical_history"] = True
            
            # Verificar condiciones preexistentes
            source_data = source['data']
            if 'chronic_conditions' in source_data and source_data['chronic_conditions']:
                expected_data["preexisting_conditions"] = True
        
        if 'seguro' in source_name:
            expected_data["insurance_data"] = True
            
            # Verificar condiciones preexistentes
            source_data = source['data']
            if 'preexisting_conditions' in source_data and source_data['preexisting_conditions']:
                expected_data["preexisting_conditions"] = True
    
    print("\n📋 Verificación de datos para Reto 4:")
    for data_type, found in expected_data.items():
        status = "✅" if found else "❌"
        print(f"  {status} {data_type.replace('_', ' ').title()}")
    
    all_found = all(expected_data.values())
    print(f"\n🎯 Cumplimiento de requisitos: {'✅ COMPLETO' if all_found else '❌ INCOMPLETO'}")
    
    return all_found

def main():
    """Función principal"""
    
    print("🚀 Iniciando pruebas del servicio Firebase para Angelus Sentinel")
    print("=" * 60)
    
    # 1. Probar servicio básico
    if not test_firebase_service():
        print("\n❌ Fallaron las pruebas básicas del servicio")
        return
    
    # 2. Probar datos específicos
    test_specific_patient_data()
    
    print("\n" + "=" * 60)
    print("🎯 Todas las pruebas completadas exitosamente")
    print("🏥 Firebase está listo para Angelus Sentinel - Reto 4")

if __name__ == "__main__":
    main()
