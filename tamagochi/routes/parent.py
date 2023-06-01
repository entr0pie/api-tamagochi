from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

# from database.Database import SQLite3Manager
from database.database import Parent, create_session
from modules.internal import checkFields

# db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/parent")
jwt = JWTManager()

@parent.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session = create_session()
    
    try:
        parent = session.query(Parent).filter(Parent.email == data['email']).one()
        session.close()
        
        if checkpw(data.get('password').encode(), parent.password):
            access_token = create_access_token(identity=data["email"])
            return jsonify(access_token=access_token)
    
    except NoResultFound:
        pass

    return { "error": "Permission Denied" }, 403

@parent.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    session = create_session()
    
    if session.query(Parent).filter(Parent.email == data.get('email')).first():
        return { "error": "Account already registered" }, 403

    data['password'] = hashpw(data['password'].encode(), gensalt())

    parent = Parent(name=data.get('name'), surname=data.get('surname'),
                    email=data.get('email'), password=data.get('password'),
                    gender=data.get('gender'))

    session.add(parent)
    session.commit()
    session.close()

    return { "status": "registered" }

# @parent.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(message=f"Hello, {current_user}. This is a protected route.")
