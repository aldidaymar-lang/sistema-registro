from flask import Flask, request, jsonify

app = Flask(__name__)

usuario = {}

@app.route('/')
def home():
    return "¡Servidor activo y funcionando!"

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    clave = data.get('clave')
    
    if not nombre or not clave:
        return jsonify({"error": "Faltan datos"}), 400
        
    usuario[nombre] = clave
    return jsonify({"mensaje": "usuario registrado con exito"}), 200

@app.route('/login', methods=['POST'])
def iniciar_seccion():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    clave = data.get('clave')
    
    if nombre in usuario and usuario[nombre] == clave:
        return jsonify({"mensaje": "¡Bienvenidos al sistema!"}), 200
    else:
        return jsonify({"error": "usuario o contraseña incorrecta"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
