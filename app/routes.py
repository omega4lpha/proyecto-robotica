from flask import jsonify, request, render_template, redirect, url_for
from app.database import create_connection
from app.models import upsert_device, get_device, get_all_devices

def init_routes(app):
    @app.route('/api/sensor', methods=['POST'])
    def receive_sensor_data():
        data = request.json
        if not data or 'id' not in data or 'value' not in data or 'state' not in data:
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            upsert_device(conn, data)
            return jsonify({"status": "success", "message": "Datos guardados"}), 200
        else:
            return jsonify({"status": "error", "message": "Error de base de datos"}), 500

    @app.route('/api/device/<string:device_id>', methods=['GET'])
    def get_device_state(device_id):
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            device = get_device(conn, device_id)
            if device:
                return jsonify({"status": "success", "device": device}), 200
            else:
                return jsonify({"status": "error", "message": "Dispositivo no encontrado"}), 404
        else:
            return jsonify({"status": "error", "message": "Error de base de datos"}), 500

    @app.route('/api/device/<string:device_id>', methods=['POST'])
    def set_device_state(device_id):
        data = request.json
        new_state = data.get("state")
        if not new_state:
            return jsonify({"status": "error", "message": "Falta el estado"}), 400

        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            device = get_device(conn, device_id)
            if device:
                device["state"] = new_state
                upsert_device(conn, device)
                return jsonify({"status": "success", "message": f"Dispositivo {device_id} actualizado a {new_state}"}), 200
            else:
                return jsonify({"status": "error", "message": "Dispositivo no encontrado"}), 404
        else:
            return jsonify({"status": "error", "message": "Error de base de datos"}), 500

    @app.route('/devices', methods=['GET'])
    def list_devices():
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            devices = get_all_devices(conn)
            return render_template('devices.html', devices=devices)
        else:
            return jsonify({"status": "error", "message": "Error de base de datos"}), 500
        
    @app.route('/control', methods=['GET'])
    def control_panel():
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            devices = get_all_devices(conn)
            return render_template('control_panel.html', devices=devices)
        else:
            return "Error de base de datos", 500
        
        # Añade estas rutas adicionales
    @app.route('/devices/create', methods=['GET'])
    def create_device_form():
        return render_template('create_device.html')

    @app.route('/devices/create', methods=['POST'])
    def create_device():
        device_id = request.form.get('device_id')
        value = float(request.form.get('value'))
        state = request.form.get('state', 'off')  # Default to 'off' if not provided
        
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            upsert_device(conn, {"id": device_id, "value": value, "state": state})
            return redirect(url_for('control_panel'))
        return "Error de base de datos", 500

    @app.route('/devices/edit/<string:device_id>', methods=['GET'])
    def edit_device_form(device_id):
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            device = get_device(conn, device_id)
            if device:
                return render_template('edit_device.html', device=device)
        return "Dispositivo no encontrado", 404

    @app.route('/devices/edit/<string:device_id>', methods=['POST'])
    def edit_device(device_id):
        value = float(request.form.get('value'))
        state = request.form.get('state', 'off')
        
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            upsert_device(conn, {"id": device_id, "value": value, "state": state})
            return redirect(url_for('control_panel'))
        return "Error de base de datos", 500

    @app.route('/devices/delete/<string:device_id>', methods=['GET'])
    def delete_device_form(device_id):
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            device = get_device(conn, device_id)
            if device:
                return render_template('delete_device.html', device=device)
        return "Dispositivo no encontrado", 404

    @app.route('/devices/delete/<string:device_id>', methods=['POST'])
    def delete_device(device_id):
        conn = create_connection(app.config['DATABASE'])
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM devices WHERE id = ?', (device_id,))
            conn.commit()
            return redirect(url_for('control_panel'))
        return "Error de base de datos", 500