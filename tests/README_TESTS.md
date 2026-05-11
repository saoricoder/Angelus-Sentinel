# Suite de Tests para Angelus Sentinel - Reto 4

## Descripción
Suite completa de tests automatizados para el sistema Angelus Sentinel, diseñada para asegurar el cumplimiento del Reto 4: Sistema de Alerta Temprana de Ingresos a Emergencias.

## Framework
- **Pytest**: Framework principal de testing
- **pytest-asyncio**: Soporte para tests asíncronos
- **pytest-mock**: Mocking de dependencias externas
- **unittest.mock**: Mocking nativo de Python

## Estructura de Tests

### 1. Admissions Endpoint (`/api/admision/emergencia`)
**Funcionalidad**: Procesamiento de admisiones de emergencia con webhook trigger

**Tests Cubiertos**:
- ✅ **Happy Path** (2 tests): Flujo normal de admisión y generación de IDs únicos
- ✅ **Edge Cases** (3 tests): Payload vacío, cédula inválida, campos faltantes, caracteres especiales
- ✅ **Error Management** (2 tests): Errores en validación de póliza y Firebase
- ✅ **Integration** (1 test): Verificación de llamadas a servicios

### 2. Chat Endpoint (`/api/chat`)
**Funcionalidad**: Interacción con agente IA Angelus para validación de pólizas

**Tests Cubiertos**:
- ✅ **Happy Path** (2 tests): Procesamiento de mensajes y pasos secuenciales
- ✅ **Edge Cases** (3 tests): Payload vacío, caracteres especiales, JSON mal formado
- ✅ **Error Management** (2 tests): Errores en servicio Gemini y métodos HTTP
- ✅ **Integration** (1 test): Llamadas a Gemini con datos correctos

### 3. Patients Endpoint (`/api/patients/{ci}`)
**Funcionalidad**: Búsqueda de pacientes por cédula con autocompletado

**Tests Cubiertos**:
- ✅ **Happy Path** (2 tests): Recuperación de pacientes existentes
- ✅ **Edge Cases** (3 tests): Pacientes inexistentes, CI inválido, CI vacío
- ✅ **Error Management** (2 tests): Errores en Firebase y excepciones generales
- ✅ **Integration** (1 test): Prioridad de búsqueda en Firebase

## Instalación y Ejecución

### Prerrequisitos
```bash
pip install -r tests/requirements.txt
```

### Ejecutar todos los tests
```bash
pytest tests/ -v
```

### Ejecutar tests por categoría
```bash
# Happy Path tests
pytest tests/ -k "test_valid" -v

# Edge Cases tests  
pytest tests/ -k "test_empty or test_invalid or test_special" -v

# Error Management tests
pytest tests/ -k "test_error" -v

# Integration tests
pytest tests/ -k "test_integration" -v
```

### Ejecutar tests por endpoint
```bash
# Admissions endpoint
pytest tests/ -k "TestAdmissions" -v

# Chat endpoint
pytest tests/ -k "TestChat" -v

# Patients endpoint
pytest tests/ -k "TestPatients" -v
```

## Mocks y Fixtures

### Fixtures Disponibles
- `valid_admission_payload`: Payload válido para admisión
- `valid_chat_payload`: Payload válido para chat
- `mock_gemini_service`: Mock del servicio Gemini Pro
- `mock_firebase_db`: Mock de la base de datos Firebase

### Mocks Implementados
- **Gemini Pro**: Simulación de respuestas de IA
- **Firebase Firestore**: Mock de consultas y operaciones de base de datos
- **HTTP Requests**: Mock de llamadas a endpoints externos

## Cobertura de Requisitos del Reto 4

### ✅ Webhook Trigger
- Tests para activación por ingreso de paciente
- Validación de payload de admisión
- Verificación de formato de cédula

### ✅ AI Agent Policy Validation
- Tests de integración con Gemini Pro
- Verificación de pasos secuenciales de validación
- Mock de respuestas de IA

### ✅ Pre-existing Conditions Check
- Tests de búsqueda en historial médico
- Verificación de consultas a Firebase
- Manejo de pacientes sin historial

### ✅ Simultaneous Notifications
- Tests de envío paralelo de notificaciones
- Verificación de llamadas a hospital y seguro
- Mock de servicios de notificación

### ✅ Chat Interface
- Tests de procesamiento de mensajes
- Verificación de pasos de validación en chat
- Manejo de caracteres especiales y errores

## Reportes

### Generar reporte de cobertura
```bash
pytest tests/ --cov=api --cov-report=html
```

### Generar reporte en formato JSON
```bash
pytest tests/ --json-report=test-results.json
```

### Ejecutar con reporte detallado
```bash
pytest tests/ -v --tb=long --html=test-report.html
```

## Integración CI/CD

### GitHub Actions (Ejemplo)
```yaml
name: Test Angelus Sentinel
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: pip install -r tests/requirements.txt
      - name: Run tests
        run: pytest tests/ -v
```

## Métricas de Calidad

### Total de Tests: 21
- Happy Path: 6 tests (28.6%)
- Edge Cases: 9 tests (42.9%)
- Error Management: 6 tests (28.6%)
- Integration: 3 tests (14.3%)

### Cobertura Esperada
- **Endpoints API**: 95%+
- **Lógica de Negocio**: 90%+
- **Manejo de Errores**: 100%

## Mantenimiento

### Agregar Nuevos Tests
1. Crear método en clase apropiada
2. Usar naming convention: `test_descripcion_escenario`
3. Agregar fixtures si es necesario
4. Documentar en este README

### Actualizar Mocks
1. Modificar fixtures correspondientes
2. Actualizar parámetros esperados
3. Verificar que todos los tests pasen

## Buenas Prácticas

### Naming Convention
- Tests descriptivos: `deberia_retornar_error_si_email_es_vacio`
- Clases agrupadas: `TestAdmissionsEndpoint`, `TestChatEndpoint`
- Fixtures claros: `valid_admission_payload`, `mock_gemini_service`

### Estructura de Tests
```python
def test_escenario_descripcion(self, fixture1, fixture2):
    """Descripción breve de lo que verifica el test"""
    # Arrange
    # Act  
    # Assert
```

### Mocking Strategy
- Mock de dependencias externas (Firebase, Gemini)
- Evitar llamadas reales a APIs
- Verificar parámetros correctos en llamadas

## Troubleshooting

### Common Issues
1. **Import Error**: Verificar PYTHONPATH incluye directorios api/ y backend/
2. **Async Tests**: Usar decorador `@pytest.mark.asyncio`
3. **Mock Not Working**: Verificar que los mocks estén correctamente configurados
4. **Fixture Not Found**: Asegurar que fixtures estén importados

### Debug Mode
```bash
pytest tests/ -v -s --pdb
```

## Contacto
Para dudas o sugerencias sobre la suite de tests, contactar al equipo de QA.
