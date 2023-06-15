from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

# from database.Database import SQLite3Manager
from database.database import Parent, Child, Task, create_session

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

@parent.route("/child/register", methods=["POST"])
@jwt_required()
def registerChild():
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    child = Child(name=data.get("name"), surname=data.get("surname"), 
                  access_token=token_hex(32), balance=0, gender=data.get("gender"),
                  id_parent_fk=parent.id)

    access_token = child.access_token

    session.add(child)
    session.commit()
    session.close()
    
    return {"child_token": access_token}


@parent.route("/child/task/register")
@jwt_required()
def registerTask():
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    

@parent.route("/child/task/delete")
@jwt_required()
def deleteTask():
    data = request.get_json()


@parent.route("/child/task/edit")
@jwt_required()
def editTask():
    data = request.get_json()



