from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)
# Aquí está el nombre exigido para tu evaluación
DB_NAME = 'usuarios_lazcano.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (usuario TEXT PRIMARY KEY, password_hash TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"mensaje": "Faltan parametros"}), 400

    pwd_hash = hash_password(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios VALUES (?, ?)", (usuario, pwd_hash))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": f"Usuario {usuario} registrado con \u00e9xito"})
    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "El usuario ya existe"}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario = ?", (usuario,))
    record = cursor.fetchone()
    conn.close()

    if record and record == hash_password(password):
        return jsonify({"mensaje": "Validaci\u00f3n exitosa"})
    else:
        return jsonify({"mensaje": "Usuario/contrase\u00f1a invalidos"}), 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
