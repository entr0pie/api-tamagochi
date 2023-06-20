from secrets import token_hex

from flask import Blueprint, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

from database.database import Parent, Child, Task, create_session

child = Blueprint("child", __name__, url_prefix="/child")

jwt = JWTManager()

@child.route("/register", methods=["POST"])
@jwt_required()
def create():
    """Create a new Child 
    (http://parent.tamagochi.up.br/docs/#/Child/post_child_register)"""
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


@child.route("/<access_token>", methods=["GET"])
@child.route("/", methods=["GET"])
@jwt_required()
def read(access_token=None):
    """Get info of a Child. If <access_token> is not set, the server will return all the childs 
    (http://parent.tamagochi.up.br/docs/#/Child/get_child)
    (http://parent.tamagochi.up.br/docs/#/Child/get_child__access_token_)"""

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

@child.route("/edit/<access_token>", methods=["PUT"])
@jwt_required()
def edit(access_token):
    """Edit Child attributes 
    (http://parent.tamagochi.up.br/docs/#/Child/put_child_edit__access_token_)"""
    
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

@child.route("/delete/<access_token>", methods=["DELETE"])
@jwt_required()
def delete(access_token):
    """Delete a Child from the database
    (http://parent.tamagochi.up.br/docs/#/Child/delete_child_delete__access_token_)"""

    session = create_session()

    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    if (child := session.query(Child).filter(and_(Child.access_token == access_token, Child.parent == parent.id)).first()) is not None:
        session.delete(child)
        session.commit()
        session.close()

        return '', 204

    return { "status" : False }, 200
