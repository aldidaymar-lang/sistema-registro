from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

usuario = {}

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
        
    usuario[nombre] = clave
    return jsonify({"mensaje": "Usuario registrado con éxito"}), 200

@app.route('/login', methods=['POST'])
def iniciar_seccion():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    clave = data.get('clave')
    
    if nombre in usuario and usuario[nombre] == clave:
        return jsonify({"mensaje": "¡Bienvenido al sistema!"}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrecta"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
