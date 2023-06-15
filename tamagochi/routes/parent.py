
from secrets import token_hex
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

@parent.route("/child", methods=["GET"])
@jwt_required()
def getChilds():
    session = create_session()
    parent_id = session.query(Parent).filter(Parent.email == get_jwt_identity()).first().id
    childs = session.query(Child).filter(Child.id_parent_fk == parent_id).all()
    
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
                  id_parent_fk=parent.id)

    access_token = child.access_token

    session.add(child)
    session.commit()
    session.close()
    
    return {"child_token": access_token}

@parent.route("/task", methods=["GET"])
@jwt_required()
def getTasks():
    session = create_session()
    parent_id = session.query(Parent).filter(Parent.email == get_jwt_identity()).first().id
    tasks = session.query(Task).filter(task.id_parent_fk == parent_id).all()
    
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
                is_visible=data.get("is_visible"), id_parent_fk=parent.id)

    session.add(task)
    session.commit()
    session.close()

    return {"status": True}

@parent.route("/task/delete")
@jwt_required()
def deleteTask():
    data = request.get_json()


@parent.route("/task/edit")
@jwt_required()
def editTask():
    data = request.get_json()



