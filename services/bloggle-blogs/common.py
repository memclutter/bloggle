from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import environments

db = SQLAlchemy()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environments[environment])

    db.init_app(app)

    from blueprints.status import status_blueprint
    from blueprints.blog import blog_blueprint

    app.register_blueprint(status_blueprint)
    app.register_blueprint(blog_blueprint)

    return app
