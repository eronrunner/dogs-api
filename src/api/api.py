from flask import Flask, jsonify
from flask_swagger import swagger


app = Flask(__name__, static_folder="../../static", template_folder="../../template")


@app.route("/spec")
def spec():
    return jsonify(swagger(app))


def register_blueprint():
    from src.api.blueprints.dogs import dogs
    from src.api.blueprints.images import images

    app.register_blueprint(dogs)
    app.register_blueprint(images)


def main():
    register_blueprint()
    app.run(debug=True)
