#!/usr/bin/python3

from secrets import token_hex
from flask import Flask
from flask_jwt_extended import JWTManager
from routes.parent import parent

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = token_hex(64)
jwt = JWTManager(app)

app.register_blueprint(parent)


if __name__ == '__main__':
    app.run()
