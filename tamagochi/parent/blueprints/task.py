from flask import Blueprint, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

from database.database import Parent, Child, Task, create_session

task = Blueprint("task", __name__, url_prefix="/task")

jwt = JWTManager()

@task.route("/register", methods=["POST"])
@jwt_required()
def create():
    """Create a new Task 
    (http://parent.tamagochi.up.br/docs/#/Task/post_task_register)"""

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

@task.route("/<id>", methods=["GET"])
@task.route("/", methods=["GET"])
@jwt_required()
def read(id=None):
    """Get info of a Task. If <id> is not set, the server will return all the tasks available 
    (http://parent.tamagochi.up.br/docs/#/Child/get_child)
    (http://parent.tamagochi.up.br/docs/#/Child/get_child__access_token_)""" 

    session = create_session()
    parent_id = session.query(Parent).filter(Parent.email == get_jwt_identity()).first().id

    if id:
        if (task := session.query(Task).filter(and_(Task.parent == parent_id, Task.id == id)).first()) is not None:
            task_data = {"id": task.id, "name":task.name, "description":task.description, 
                         "period": task.period, "frequency":task.frequency, 
                         "is_visible":task.is_visible}
    
            return task_data 

        return { "error" : "There's no task with this id" }, 404

    tasks = session.query(Task).filter(Task.parent == parent_id).all()
    
    response = [] 

    for task in tasks:
        task_data = {"id":task.id, "name":task.name, "description":task.description, 
                      "period": task.period, "frequency":task.frequency, 
                      "is_visible":task.is_visible}
        
        response.append(task_data)

    return response 

@task.route("/edit/<id>", methods=["PUT"])
@jwt_required()
def update(id):
    """Update the attributes of a Task 
    (http://parent.tamagochi.up.br/docs/#/Task/put_task_edit__id_)"""

    data = request.get_json()
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    if (task := session.query(Task).filter(and_(Task.parent == parent.id, Task.id == id)).first()) is not None:
        updated_data = request.get_json()
        
        for key in updated_data:
            setattr(task, key, updated_data[key])

        session.commit()
        session.close()
    
        return { "status" : True }, 200

    return { "error" : "There's no task with this id" }, 404

@task.route("/delete/<id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    """Delete a Task 
    (http://parent.tamagochi.up.br/docs/#/Task/delete_task_delete__id_)"""
    
    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()

    if (task := session.query(Task).filter(and_(Task.parent == parent.id, Task.id == id)).first()) is not None:
        session.delete(task)
        session.commit()
        session.close()
        
        return '', 204

    return { "error" : "There's no task with this id" }, 404


