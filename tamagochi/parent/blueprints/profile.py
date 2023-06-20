
from flask import Blueprint, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

from database.database import Parent, Child, Task, create_session
from modules.internal import verifyFields

profile = Blueprint("profile", __name__, url_prefix="/")

jwt = JWTManager()

@profile.route("/login", methods=["POST"])
def login():
    """Authenticate in the server
    (http://parent.tamagochi.up.br/docs/#/Profile/post_login)"""
    
    data = request.get_json()
    
    if not verifyFields(data, ('email', 'password')):
        return { "error": "Missing fields" }, 400
    
    session = create_session()
    
    try:
        parent = session.query(Parent).filter(Parent.email == data['email']).one()
        session.close()
        
        if checkpw(data.get('password').encode(), parent.password.encode()):
            access_token = create_access_token(identity=data["email"])
            return { "access_token" : access_token }, 200
    
    except NoResultFound:
        return { "error": "Permission Denied" }, 403

@profile.route("/register", methods=["POST"])
def create():
    """Register a Parent in the database
    (http://parent.tamagochi.up.br/docs/#/Profile/post_register)"""
    
    data = request.get_json()
    
    if not verifyFields(data, ('name', 'surname', 'email', 'password', 'gender')):
        return { "error": "Missing fields" }, 400

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

    return { "status": "registered" }, 200

@profile.route("/profile", methods=["GET"])
@jwt_required()
def read():
    """Get Parent information
    (http://parent.tamagochi.up.br/docs/#/Profile/get_profile)"""

    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    return {"email": parent.email, "name": parent.name, "surname": parent.surname, "gender":parent.gender}, 200

@profile.route("/profile/edit", methods=["PUT"])
@jwt_required()
def update():
    """Update Parent data 
    (http://parent.tamagochi.up.br/docs/#/Profile/put_profile_edit)"""

    updated_data = request.get_json()
    
    if "id" in updated_data.keys():
        updated_data.pop('id')

    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    for key in updated_data:
        setattr(parent, key, updated_data[key])
    
    session.commit()
    session.close()

    return { "status" : True }, 200

@profile.route("/profile/delete", methods=["DELETE"])
@jwt_required()
def delete():
    """Delete Parent account 
    (http://parent.tamagochi.up.br/docs/#/Profile/delete_profile_delete)"""

    session = create_session()
    parent = session.query(Parent).filter(Parent.email == get_jwt_identity()).first()
    
    childs = session.query(Child).filter(Child.parent == parent.id).all()

    for child in childs:
        session.delete(child)

    session.delete(parent)
    session.commit()
    session.close()

    return '', 204
