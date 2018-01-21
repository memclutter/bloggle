import requests
from flask import Flask
from flask_jwt_extended import JWTManager

from config import environments

jwt = JWTManager()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environments[environment])

    jwt.init_app(app)

    from blueprints.status import status_blueprint
    from blueprints.account import account_blueprint

    app.register_blueprint(status_blueprint)
    app.register_blueprint(account_blueprint)

    return app


class ServiceClient(object):

    @staticmethod
    def _process_response(response: requests.Response):
        status_code = response.status_code
        is_json = response.headers.get('content-type') == 'application/json'
        body = response.json() if is_json else response.text
        success = body['success'] if is_json and ('success' in body) else False
        data = body['data'] if is_json and ('data' in body) else None
        message = body['message'] if is_json and ('message' in body) else 'Internal server error'

        if status_code >= 500:
            raise RuntimeError(message)

        return success, data, message

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get(self, path, params=None):
        url = self._create_url(path)
        response = requests.get(url, params)

        return self._process_response(response)

    def post(self, path, data):
        url = self._create_url(path)
        response = requests.post(url, json=data)

        return self._process_response(response)

    def _create_url(self, path):
        return '/'.join([
            str(self.endpoint).rstrip('/'),
            str(path).lstrip('/'),
        ])
