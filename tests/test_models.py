from app.models import create_table, upsert_device, get_device
from app.database import create_connection

def test_upsert_and_get_device():
    # Usar base de datos en memoria para pruebas
    conn = create_connection(":memory:")
    create_table(conn)  # Asegurar que la tabla existe
    
    device = {"id": "sensor_1", "value": 25.0, "state": "off"}
    
    # Insertar dispositivo
    upsert_device(conn, device)
    result = get_device(conn, "sensor_1")
    assert result == device
    
    # Actualizar dispositivo
    device["state"] = "on"
    upsert_device(conn, device)
    result = get_device(conn, "sensor_1")
    assert result == device
    
    # Dispositivo no existente
    result = get_device(conn, "sensor_2")
    assert result is None