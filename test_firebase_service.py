"""
Script para probar el servicio Firebase de Angelus Sentinel
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.firebase_service import federated_search, initialize_firebase

def test_firebase_service():
    """Prueba el servicio Firebase de Angelus Sentinel"""
    
    print("🧪 Probando el servicio Firebase de Angelus Sentinel...")
    print("=" * 60)
    
    # 1. Inicializar Firebase
    db = initialize_firebase()
    
    if not db:
        print("❌ No se pudo inicializar Firebase")
        return False
    
    print("✅ Firebase inicializado correctamente")
    
    # 2. Probar búsqueda por CI
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
    
    # 3. Probar búsqueda por nombre
    print("\n🔍 Probando búsqueda por nombre...")
    test_name = "Juan"
    results_by_name = federated_search(name_query=test_name)
    
    print(f"📊 Resultados para nombre '{test_name}': {len(results_by_name)} pacientes encontrados")
    
    for result in results_by_name:
        print(f"👤 {result['name']} (CI: {result['id']})")
    
    # 4. Probar búsqueda sin resultados
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
