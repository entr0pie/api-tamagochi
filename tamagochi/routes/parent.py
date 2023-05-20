from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from database.Database import SQLite3Manager
from modules.internal import checkFields

db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/parent")
jwt = JWTManager()

@parent.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = db.query("SELECT count(*) FROM pai WHERE email = ? AND senha = ?", (data['email'], data['password']))
    print(result)
    if result[0][0] == 1:
        access_token = create_access_token(identity=data["email"])
        return jsonify(access_token=access_token)
    
    return "not here.", 403

@parent.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}. This is a protected route.")

@parent.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name, surname = data.get('name'), data.get('surname')
    email, password = data.get('email'), data.get('password')
    gender = data.get('gender')

    db.query('INSERT INTO pai (nome, sobrenome, email, senha, sexo) VALUES (?, ?, ?, ?, ?)',
             (name, surname, email, password, gender), type="change")

    return { "status": "registered" }
