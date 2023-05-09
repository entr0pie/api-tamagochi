#!/bin/python 

from json import loads

from flask import Blueprint
from flask import request, jsonify

from database.Authenticator import authParent, registerParent
from database.Authenticator import checkPostRequest

parent = Blueprint("parent", __name__)

# Sign up, Login and reset password # 
@parent.route("/parent/register", methods=["POST"])
def createAccount():
    data = request.get_json()
    
    if not checkPostRequest(data, ("email", "name", "surname", "password", "gender")):
        return "Your request sucks!", 400
   
    status = registerParent(data.get('email'), data.get('name'), 
                            data.get('surname'), data.get('password'), data.get('gender'))
    
    if status:
        return "Successfully registered!"

    else: 
        return "Oh shit."

@parent.route('/parent/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not checkPostRequest(data, ("user", "password")):
        return "Your request sucks!", 400

    if (authParent(data.get('user'), data.get('password'))):
        return "You're logged in!"
    
    return "Permission Denied", 403

@parent.route("/parent/reset_password", methods=["POST"])
def resetPassword():
    return "";

# Child Management #
@parent.route("/child/child", methods=["GET"])
def checkChild():
    cursor = get_cursor()
    res = cursor.execute("PRAGMA table_info(pai)")
    return str(res.fetchall())

@parent.route("/child/add", methods=["POST"])
def addChild():
    return "";

@parent.route("/child/edit", methods=["POST"])
def editChild():
    return "";

@parent.route("/child/delete", methods=["POST"])
def deleteChild():
    return "";

# Task Management #
@parent.route("/child/task/", methods=["GET"])
def checkTask():
    return "";

@parent.route("/child/task/add", methods=["POST"])
def addTask():
    return ""

@parent.route("/child/task/edit", methods=["POST"])
def editTask():
    return ""

@parent.route("/child/task/delete", methods=["POST"])
def deleteTask():
    return ""
