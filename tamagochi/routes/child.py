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

@child.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session = create_session()
    
    try:
        child = session.query(Child).filter(Child.access_token == data.get("access_token")).one()
    
    except NoResultFound:
        return { "error": "Permission denied" }, 403

    jwt_token = create_access_token(identity=data.get("access_token"))
    return jsonify(jwt_token=jwt_token)

