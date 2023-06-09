from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import and_, or_ 
from sqlalchemy.exc import NoResultFound

from bcrypt import hashpw, gensalt, checkpw 

from flasgger import swag_from

# from database.Database import SQLite3Manager
from database.database import Parent, Child, Task, create_session
from modules.internal import checkFields

# db = SQLite3Manager("./database/database.db")
parent = Blueprint("parent", __name__, url_prefix="/parent")

jwt = JWTManager()

@parent.route("/login", methods=["POST"])
def login():
    """Login as a Parent
    Authenticate in the application through email and password, as a Parent. 
    ---
    parameters:
        - name: requestBody
          in: body
          description: JSON object with email and password.
          required: true
          schema:
            type: object 
            properties:
                email:
                    type: string
                password:
                    type: string
    responses:
        200:
            description: Login successfull. Returns a JSON with a \"access_token\" key, contaning the JWT.
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                example:
                    access_token: JWT_TOKEN 
        403:
            description: Email or password incorrect. Returns a error message.
            schema:
                type: object 
                properties:
                    error:
                        type: string
                example:
                    error: Permission Denied
    """

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
    """Register a Parent
    Register a new Parent in the Database, if not registered. 
    ---
    parameters:
      - name: requestBody 
        in: body
        description: JSON object with name, surname, email, password and gender.
        required: true
        schema:
            type: object
            properties:
                name:
                    type: string
                surname:
                    type: string
                email:
                    type: string
                password:
                    type: string
                gender:
                    type: string
                    enum: ['m', 'f', 'n']
    responses:
      403:
        description: Account already registered. Returns a JSON object with the error.
        schema:
            type: object
            properties:
              error:
                type: string
            example:
                error: Account already registered

      200:
        description: Account created successfully. Returns a JSON object with the status.
        schema:
            type: object 
            properties:
                status:
                    type: string
            example:
                status: registered
    """
    
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
    """Register a Child.
    Register a new Child in the Database, linked to it's Parent.
    parameters:
      - name: requestBody 
        in: body
        description: JSON object with name, surname, and gender of the Child.
        required: true
        schema:
            type: object
            properties:
                name:
                    type: string
                surname:
                    type: string
                gender:
                    type: string
                    enum: ['m', 'f', 'n']

    responses:
        200:
            description: Child registered successfully.
            schema:
                type: object 
                properties:
                    child_token:
                        type: string
                example:
                    child_token: 32_BYTES_TOKEN

    """ 

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



