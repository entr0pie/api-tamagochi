from flask import Blueprint, request, current_app
from flask_jwt_extended import JWTManager, create_access_token

from database.Database import SQLite3Manager

db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/parent")
jwt = JWTManager()

@parent.record_once
def on_load(state):
    jwt.init_app(state.app)

def checkFields(data_obj, *fields):
    for value in fields:
        if data_obj.get(value) is None:
            return False

    return True

@parent.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if checkFields(data, 'password', 'email'):
        return {'error': 'missing fields'}, 400

    email, password = data.get('email'), data.get('password')
    entries_found = db.query('SELECT COUNT(*) FROM pai WHERE email = ? AND senha = ?', (email, password))[0][0]

    if entries_found == 1:
        access_token = create_access_token(identity=email)
        return {'access_token': access_token}, 200
    else:
        return {'error': 'Invalid email or password'}, 401

@parent.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name, surname = data.get('name'), data.get('surname')
    email, password = data.get('email'), data.get('password')
    gender = data.get('gender')

    db.query('INSERT INTO pai (nome, sobrenome, email, senha, sexo) VALUES (?, ?, ?, ?, ?)',
             (name, surname, email, password, gender), type="change")

    return { "status": "registered" }


