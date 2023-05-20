from flask import Blueprint, request, current_app
from flask_jwt_extended import JWTManager, create_access_token

from database.Database import SQLite3Manager

db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/parent")
jwt = JWTManager()

@parent.record_once
def on_load(state):
    jwt.init_app(state.app)

@parent.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    entries_found = db.select('SELECT COUNT(*) FROM pai WHERE email = ? AND senha = ?', (email, password))[0][0]

    if entries_found == 1:
        access_token = create_access_token(identity=email)
        return {'access_token': access_token}, 200
    else:
        return {'error': 'Invalid email or password'}, 401
    
