
import logging as log
from secrets import token_hex
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

# from database.Database import SQLite3Manager
from database.database import Parent, Child, Task, create_session

# db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/")

jwt = JWTManager()

@parent.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session = create_session()
    
    try:
        parent = session.query(Parent).filter(Parent.email == data['email']).one()
        session.close()
        
        if checkpw(data.get('password').encode(), parent.password.encode()):
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

@parent.route("/profile", methods=["GET"])
@jwt_required()
def getParentInfo():
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    return {"email": parent.email, "name": parent.name, "surname": parent.surname, "gender":parent.gender}, 200

@parent.route("/profile/edit", methods=["PUT"])
@jwt_required()
def update():
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    updated_data = request.get_json()

    for key in updated_data:
        setattr(parent, key, updated_data[key])
    
    session.commit()
    session.close()

    return { "status" : True }, 200

@parent.route("/profile/delete", methods=["DELETE"])
@jwt_required()
def delete():
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    childs = session.query(Child).filter(Child.parent == parent.id).all()

    for child in childs:
        session.delete(child)

    session.delete(parent)
    session.commit()
    session.close()

    return '', 204

@parent.route("/child/<access_token>", methods=["GET"])
@parent.route("/child", methods=["GET"])
@jwt_required()
def getChilds(access_token=None):
    session = create_session()
    parent_id = session.query(Parent).filter(Parent.email == get_jwt_identity()).first().id
    
    if access_token:
        child = session.query(Child).filter(and_(Child.parent == parent_id, Child.access_token == access_token)).first()
        
        return {"name": child.name, "surname":child.surname, 
                "access_token":child.access_token, "balance":child.balance, 
                "gender":child.gender}, 200
    
    childs = session.query(Child).filter(Child.parent == parent_id).all()
    
    response = [] 

    for child in childs:
        child_data = {"name":child.name, "surname":child.surname, 
                      "access_token": child.access_token, "balance":child.balance, 
                      "gender":child.gender}
        
        response.append(child_data)

    return response 

@parent.route("/child/register", methods=["POST"])
@jwt_required()
def registerChild():
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    child = Child(name=data.get("name"), surname=data.get("surname"), 
                  access_token=token_hex(32), balance=0, gender=data.get("gender"),
                  parent=parent.id)

    access_token = child.access_token

    session.add(child)
    session.commit()
    session.close()
    
    return {"child_token": access_token}

@parent.route("/child/edit/<access_token>", methods=["PUT"])
@jwt_required()
def editChild(access_token):
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
   
    if (child := session.query(Child).filter(Child.parent == parent.id).first()) is not None:
        updated_data = request.get_json()

        for key in updated_data:
            setattr(child, key, updated_data[key])
    
        session.commit()
        session.close()

        return { "status" : True }, 200


    return { "status" : False }, 403


@parent.route("/child/delete/<access_token>", methods=["DELETE"])
@jwt_required()
def deleteChild(access_token=None):
    session = create_session()

    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    child = session.query(Child).filter(and_(Child.access_token == access_token, Child.parent == parent.id)).first()

    session.delete(child)
    session.commit()
    session.close()

    return '', 204

@parent.route("/task/<id>", methods=["GET"])
@parent.route("/task", methods=["GET"])
@jwt_required()
def getTask(id=None):
    session = create_session()
    parent_id = session.query(Parent).filter(Parent.email == get_jwt_identity()).first().id
    tasks = session.query(Task).filter(Task.parent == parent_id).all()
    
    response = [] 

    for task in tasks:
        task_data = {"name":task.name, "description":task.description, 
                      "period": task.period, "frequency":task.frequency, 
                      "is_visible":task.is_visible}
        
        response.append(task_data)

    return response 

@parent.route("/task/register", methods=["POST"])
@jwt_required()
def registerTask():
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    task = Task(name=data.get("name"), description=data.get("description"), 
                period=data.get("period"), frequency=data.get("frequency"), 
                is_visible=data.get("is_visible"), parent=parent.id)

    session.add(task)
    session.commit()
    session.close()

    return {"status": True}

@parent.route("/task/edit/<id>", methods=["PUT"])
@jwt_required()
def editTask(id):
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    if (task := session.query(Task).filter(and_(Task.parent == parent.id, Task.id == id))) is not None:
        updated_data = request.get_json()
        
        for key in updated_data:
            setattr(task, key, updated_data[key])

        session.commit()
        session.close()
    
        return { "status" : True }, 200

    return { "status" : False }, 403

@parent.route("/task/delete/<id>")
@jwt_required()
def deleteTask(id):
    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()

    if (task := session.query(Task).filter(and_(Task.parent == parent.id, Task.id == id))) is not None:
        session.delete(task)
        session.commit()
        session.close()
        
        return '', 204

    return { "status" : False }, 403


