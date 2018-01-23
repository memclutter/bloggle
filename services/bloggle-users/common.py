from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import environments
from helpers import format_response

db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environments[environment])
    app.after_request(format_response)

    db.init_app(app)

    from blueprints.status import status_blueprint
    from blueprints.user import user_blueprint

    app.register_blueprint(status_blueprint)
    app.register_blueprint(user_blueprint)

    return app
