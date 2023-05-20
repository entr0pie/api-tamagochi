#!/usr/bin/python3

from flask import Flask

from modules.parent import parent
# from modules.child import child

app = Flask("tamagochi")
app.register_blueprint(parent)

# @app.route("/", methods=["GET"])
# def mainRoute():
#     return ""

# app.register_blueprint(child)


