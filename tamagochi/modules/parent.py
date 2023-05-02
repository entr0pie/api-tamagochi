#!/bin/python 

from flask import Blueprint
import sqlite3

parent = Blueprint("parent", __name__)

# Sign up, Login and reset password # 
@parent.route("/parent/register", methods=["POST"])
def createAccount():
     return "";

@parent.route("/parent/login", methods=["POST"])
def login():
    return "";

@parent.route("/parent/reset_password", methods=["POST"])
def resetPassword():
    return "";

# Child Management #
@parent.route("/child/child", methods=["GET"])
def checkChild():
    return "";

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
