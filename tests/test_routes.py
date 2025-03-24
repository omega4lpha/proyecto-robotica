import pytest
from app import create_app
from app.database import create_connection

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            create_connection()  # Crear la base de datos de prueba
        yield client

def test_receive_sensor_data(client):
    # Caso 1: Datos válidos
    response = client.post('/api/sensor', json={
        "id": "sensor_1",
        "value": 25,
        "state": "off"
    })
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Datos guardados"}

    # Caso 2: Datos incompletos
    response = client.post('/api/sensor', json={
        "id": "sensor_1",
        "value": 25
    })
    assert response.status_code == 400
    assert response.json == {"status": "error", "message": "Datos incompletos"}

def test_get_device_state(client):
    # Caso 1: Dispositivo existente
    client.post('/api/sensor', json={
        "id": "sensor_1",
        "value": 25,
        "state": "off"
    })
    response = client.get('/api/device/sensor_1')
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "device": {"id": "sensor_1", "value": 25, "state": "off"}
    }

    # Caso 2: Dispositivo no existente
    response = client.get('/api/device/sensor_2')
    assert response.status_code == 404
    assert response.json == {"status": "error", "message": "Dispositivo no encontrado"}

def test_set_device_state(client):
    # Caso 1: Cambiar estado a "on"
    client.post('/api/sensor', json={
        "id": "sensor_1",
        "value": 25,
        "state": "off"
    })
    response = client.post('/api/device/sensor_1', json={"state": "on"})
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Dispositivo sensor_1 actualizado a on"
    }

    # Caso 2: Estado no proporcionado
    response = client.post('/api/device/sensor_1', json={})
    assert response.status_code == 400
    assert response.json == {"status": "error", "message": "Falta el estado"}

    # Caso 3: Dispositivo no existente
    response = client.post('/api/device/sensor_2', json={"state": "on"})
    assert response.status_code == 404
    assert response.json == {"status": "error", "message": "Dispositivo no encontrado"}