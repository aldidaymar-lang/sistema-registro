from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Estructura de usuarios: admin, guardian, edicion, lectura
usuarios = {
    "aldimar": {"clave": "1234", "rol": "admin", "estado": "activo"}
}

# Historial de accesos e intentos de intrusión
historial_accesos = []
bloqueados = set()

CORREO_ADMIN = "aldi.daymar@gmail.com"

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

    # Por defecto se registran en modo lectura
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

        return jsonify({
            "error": "Credenciales incorrectas. Alerta de seguridad registrada.",
            "alerta": True
        }), 401

@app.route('/obtener_auditoria', methods=['POST'])
def obtener_auditoria():
    data = request.get_json() or {}
    admin_req = data.get('admin')

    rol_solicitante = usuarios.get(admin_req, {}).get('rol')
    if rol_solicitante not in ['admin', 'guardian']:
        return jsonify({"error": "No tienes permisos de auditoría."}), 403

    lista_usuarios = [{"nombre": u, "rol": datos["rol"]} for u, datos in usuarios.items()]

    return jsonify({
        "historial": historial_accesos[::-1],
        "usuarios": lista_usuarios,
        "mi_rol": rol_solicitante
    }), 200

@app.route('/cambiar_rol', methods=['POST'])
def cambiar_rol():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')
    nuevo_rol = data.get('rol')

    # Solo usuarios con rol 'admin' pueden cambiar permisos y promover a nuevos administradores
    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado. Se requiere nivel Administrador."}), 403

    if usuario_objetivo in usuarios:
        usuarios[usuario_objetivo]['rol'] = nuevo_rol
        
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        historial_accesos.append({
            "usuario": admin_req,
            "evento": f"Cambio de Rol de '{usuario_objetivo}' a '{nuevo_rol}'",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "tipo": "info"
        })
        
        return jsonify({"mensaje": f"Rol de {usuario_objetivo} actualizado a {nuevo_rol}"}), 200
    
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/bloquear_intruso', methods=['POST'])
def bloquear_intruso():
    data = request.get_json() or {}
    admin_req = data.get('admin')
    usuario_objetivo = data.get('usuario')

    if usuarios.get(admin_req, {}).get('rol') != 'admin':
        return jsonify({"error": "Acceso denegado. Se requiere nivel Administrador."}), 403

    bloqueados.add(usuario_objetivo)
    return jsonify({"mensaje": f"Usuario {usuario_objetivo} bloqueado exitosamente."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
