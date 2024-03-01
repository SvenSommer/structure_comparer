from flask import Flask, jsonify
from flask_swagger import swagger

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/spec", methods=["GET"])
def spec():
    swag = swagger(app)
    swag["info"]["version"] = "1.0"
    swag["info"]["title"] = "My API"
    return jsonify(swag)
