#!/bin/python 

from secrets import token_hex 

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from database.database import Parent, Child, create_session
from modules.internal import checkFields

child = Blueprint("child", __name__, url_prefix="/child")
jwt = JWTManager()

""" 
The child routes really need the JWT?
"""

@child.route("/register", methods=["POST"])
@jwt_required()
def register():
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
    
    return access_token

@child.route("/login", methods=["POST"])
@jwt_required()
def login():
    data = request.get_json()
    session = create_session()
    
    try:
        child = session.query(Child).filter(Child.access_token == data.get("access_token")).one()
    
    except NoResultFound:
        return { "error": "Permission denied" }, 403

    jwt_token = create_access_token(identity=data.get("access_token"))
    return jsonify(jwt_token=jwt_token)

