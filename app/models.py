from app.database import create_connection

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id TEXT PRIMARY KEY,
                value REAL,
                state TEXT
            )
        ''')
        conn.commit()
        print("Tabla 'devices' creada o ya existe")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def upsert_device(conn, device):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO devices (id, value, state)
            VALUES (?, ?, ?)
        ''', (device['id'], device['value'], device['state']))
        conn.commit()
        print(f"Dispositivo {device['id']} actualizado")
    except Error as e:
        print(f"Error al insertar/actualizar dispositivo: {e}")

def get_device(conn, device_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM devices WHERE id = ?', (device_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "value": row[1], "state": row[2]}
        else:
            return None
    except Error as e:
        print(f"Error al obtener dispositivo: {e}")
        return None
    
def get_all_devices(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM devices')
        rows = cursor.fetchall()
        devices = []
        for row in rows:
            devices.append({"id": row[0], "value": row[1], "state": row[2]})
        return devices
    except Error as e:
        print(f"Error al obtener dispositivos: {e}")
        return []