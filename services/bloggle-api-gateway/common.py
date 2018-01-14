from flask import Flask

from config import environments


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environments[environment])

    from blueprints.status import status_blueprint

    app.register_blueprint(status_blueprint)

    return app
