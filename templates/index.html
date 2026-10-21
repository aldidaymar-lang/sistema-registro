from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Usuarios iniciales con roles y estados
usuarios = {
    "aldimar": {"clave": "1234", "rol": "admin", "estado": "activo"}
}

# Historial de accesos, bloqueados y solicitudes de recuperación
historial_accesos = []
bloqueados = set()
solicitudes_recuperacion = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    clave = data.get('clave')
    
    if not nombre or not clave:
        return jsonify({"error": "Faltan datos"}), 400
        
    if nombre in usuarios:
        return jsonify({"error": "El usuario ya existe"}), 400

    usuarios[nombre] = {"clave": clave, "rol": "lectura", "estado": "activo"}
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    historial_accesos.append({
        "usuario": nombre,
        "evento": "Registro de usuario",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "tipo": "info"
    })
    
    return jsonify({"mensaje": "Usuario registrado con éxito (Rol: Lectura)"}), 200

@app.route('/login', methods=['POST'])
def iniciar_seccion():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    clave = data.get('clave')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if nombre in bloqueados or ip in bloqueados:
        return jsonify({"error": "Acceso bloqueado por seguridad."}), 403

    if nombre in usuarios and usuarios[nombre]["clave"] == clave:
        rol = usuarios[nombre]["rol"]
        historial_accesos.append({
            "usuario": nombre,
            "evento": "Inicio de Sesión Exitoso",
            "fecha": fecha_hora,
            "ip": ip,
            "tipo": "exito"
        })
        return jsonify({
            "mensaje": f"¡Bienvenido {nombre}!",
            "usuario": nombre,
            "rol": rol
        }), 200
    else:
        historial_accesos.append({
            "usuario": nombre,
            "evento": "ALERTA: Intento de Intrusión (Clave Incorrecta)",
            "fecha": fecha_hora,
            "ip": ip,
            "tipo": "alerta"
        })
        return jsonify({"error": "Credenciales incorrectas."}), 401

@app.route('/logout', methods=['POST'])
def cerrar_sesion():
    data = request.get_json() or {}
    nombre = data.get('usuario')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if nombre:
        historial_accesos.append({
            "usuario": nombre,
            "evento": "Cierre de Sesión Voluntario",
            "fecha": fecha_hora,
            "ip": ip,
            "tipo": "info"
        })

    return jsonify({"mensaje": "Sesión cerrada correctamente."}), 200

@app.route('/solicitar_recuperacion', methods=['POST'])
def solicitar_recuperacion():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({"error": "Indique su usuario para recuperación."}), 400

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    solicitudes_recuperacion.append({
        "usuario": nombre,
        "fecha": fecha_hora,
        "estado": "Pendiente"
    })

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    historial_accesos.append({
        "usuario": nombre,
        "evento": "Solicitud de Recuperación de Credenciales",
        "fecha": fecha_hora,
        "ip": ip,
        "tipo": "alerta"
    })

    return jsonify({"mensaje": "Solicitud enviada al Administrador. Espere su asistencia."}), 200

@app.route('/obtener_auditoria', methods=['POST'])
def obtener_auditoria():
    data = request.get_json() or {}
    admin_req = data.get('admin')

    rol_solicitante = usuarios.get(admin_req, {}).get('rol')
    if rol_solicitante not in ['admin', 'guardian']:
        return jsonify({"error": "Sin permisos de auditoría."}), 403

    lista_usuarios = [{"nombre": u, "rol": datos["rol"]} for u, datos in usuarios.items()]

    return jsonify({
        "historial": historial_accesos[::-1],
        "usuarios": lista_usuarios,
        "solicitudes": solicitudes_recuperacion[::-1],
        "mi_rol": rol_solicitante
    }), 200

@app.route('/resetear_clave', methods=['POST'])
def resetear_clave():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')
    nueva_clave = data.get('nueva_clave', '123456')

    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado."}), 403

    if usuario_objetivo in usuarios:
        usuarios[usuario_objetivo]['clave'] = nueva_clave
        for sol in solicitudes_recuperacion:
            if sol['usuario'] == usuario_objetivo:
                sol['estado'] = 'Atendida'
        return jsonify({"mensaje": f"Clave de {usuario_objetivo} reseteada a: {nueva_clave}"}), 200

    return jsonify({"error": "Usuario no encontrado."}), 404

@app.route('/cambiar_rol', methods=['POST'])
def cambiar_rol():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')
    nuevo_rol = data.get('rol')

    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado."}), 403

    if usuario_objetivo in usuarios:
        usuarios[usuario_objetivo]['rol'] = nuevo_rol
        return jsonify({"mensaje": f"Rol actualizado a {nuevo_rol}"}), 200
    
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')

    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado. Solo Administradores pueden eliminar usuarios."}), 403

    if usuario_objetivo in usuarios:
        del usuarios[usuario_objetivo]
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        historial_accesos.append({
            "usuario": admin_req,
            "evento": f"Eliminación definitiva del usuario '{usuario_objetivo}'",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "tipo": "alerta"
        })
        return jsonify({"mensaje": f"Usuario {usuario_objetivo} eliminado permanentemente."}), 200

    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/bloquear_intruso', methods=['POST'])
def bloquear_intruso():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')

    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado."}), 403

    bloqueados.add(usuario_objetivo)
    return jsonify({"mensaje": f"Usuario {usuario_objetivo} bloqueado."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
