from secrets import token_hex

from flask import Flask, redirect, send_from_directory
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from blueprints.child import child

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = token_hex(64)
jwt = JWTManager(app)

app.register_blueprint(child)

@app.route("/", methods=["GET"])
def sendToDocs():
    return redirect("/docs")

@app.route("/static/<path:filename>")
def serverStatic():
    return send_from_directory("./static", safe_join(getcwd(), filename))

FLASK_ROUTE = "/docs"
SWAGGER_FILE = "/static/swagger.yml"

swaggerui = get_swaggerui_blueprint(FLASK_ROUTE, SWAGGER_FILE)
app.register_blueprint(swaggerui)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)
