import os
import sys
import json

# Añadir el path raíz para importar módulos del backend
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.services.firebase_service import db

def init_mock_data():
    if not db:
        print("Error: No se pudo conectar a Firestore. Revisa tu .env")
        return

    print("Iniciando carga de datos de prueba...")

    # 1. Pacientes
    patients = [
        {"id": "PAT-001", "name": "Miguel Herrera", "policy_id": "POL-100", "age": 30},
        {"id": "PAT-002", "name": "Elena Paz", "policy_id": "POL-200", "age": 45},
        {"id": "PAT-003", "name": "Juan Perez", "policy_id": "POL-300", "age": 25},
        {"id": "PAT-004", "name": "Roberto Gomez", "policy_id": "POL-400", "age": 60},
        {"id": "PAT-005", "name": "Ana Lucia", "policy_id": "POL-500", "age": 35}
    ]

    for p in patients:
        db.collection("patients").document(p["id"]).set(p)
        print(f"Paciente {p['id']} creado.")

    # 2. Pólizas
    policies = [
        {
            "id": "POL-100",
            "status": "active",
            "plan": "Premium Gold",
            "coverage": ["Emergencias", "Cirugías", "Hospitalización", "Cardiología"],
            "exclusions": ["Cirugía estética"],
            "pre_existing_conditions": []
        },
        {
            "id": "POL-200",
            "status": "active",
            "plan": "Silver Basic",
            "coverage": ["Consultas", "Emergencias", "Traumatología"],
            "exclusions": ["Cirugías mayores", "Neurología"],
            "pre_existing_conditions": ["Diabetes", "Hipertensión"]
        },
        {
            "id": "POL-300",
            "status": "inactive",
            "plan": "Bronze",
            "coverage": [],
            "exclusions": ["Todo"],
            "pre_existing_conditions": []
        },
        {
            "id": "POL-400",
            "status": "active",
            "plan": "Senior Care",
            "coverage": ["Emergencias", "Geriatría", "Fisioterapia"],
            "exclusions": ["Deportes extremos"],
            "pre_existing_conditions": ["Artritis"]
        },
        {
            "id": "POL-500",
            "status": "active",
            "plan": "Maternidad Plus",
            "coverage": ["Obstetricia", "Neonatología", "Emergencias"],
            "exclusions": ["Tratamientos dentales complejos"],
            "pre_existing_conditions": []
        }
    ]

    for pol in policies:
        db.collection("policies").document(pol["id"]).set(pol)
        print(f"Póliza {pol['id']} creada.")

    print("Carga de datos completada con éxito.")

if __name__ == "__main__":
    init_mock_data()
