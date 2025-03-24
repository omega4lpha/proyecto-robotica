import sqlite3
from sqlite3 import Error

def create_connection(db_file='data/domotica.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Conexión a SQLite establecida")
        return conn
    except Error as e:
        print(f"Error al conectar a SQLite: {e}")
    return conn

