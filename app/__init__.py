from flask import Flask
from app.database import create_connection
import os

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'data/domotica.db'

    # Especificar la ruta de la carpeta de plantillas y archivos estáticos
    app.template_folder = os.path.abspath('templates')
    app.static_folder = os.path.abspath('static')  # Añade esta línea

    # Inicializar la base de datos
    with app.app_context():
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            from app.models import create_table
            create_table(conn)
        else:
            raise RuntimeError("Error al conectar a la base de datos")

    # Registrar rutas
    from app.routes import init_routes
    init_routes(app)

    return app