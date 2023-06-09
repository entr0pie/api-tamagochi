#!/usr/bin/python3

from secrets import token_hex
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from routes.parent import parent
from routes.child import child

app = Flask(__name__)

swagger = Swagger(app)
app.config['SWAGGER'] = {
    'title': 'OA3 Callbacks',
    'openapi': '3.0.2'
}
# app.config['SWAGGER']['openapi'] = '3.0.2'

app.config['JWT_SECRET_KEY'] = token_hex(64)
jwt = JWTManager(app)

for keys in app.config.keys():
    print(keys)

app.register_blueprint(parent)
app.register_blueprint(child)

if __name__ == '__main__':
    app.run()
