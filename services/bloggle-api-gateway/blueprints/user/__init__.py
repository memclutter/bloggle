import re
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from common import ServiceClient

user_blueprint = Blueprint('users', __name__, url_prefix='/users')


@user_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200


@user_blueprint.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    if not data:
        return jsonify('Invalid payload'), 400

    users_endpoint = current_app.config['ENDPOINTS']['users']
    users = ServiceClient(users_endpoint)

    success, status_code, data, message = users.post('/users', data)
    if success:
        # TODO: user activation
        return jsonify(data), status_code
    else:
        return jsonify(dict(data=data, message=message)), status_code


@user_blueprint.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if not data:
        return jsonify(dict(success=False, message='Invalid payload')), 400

    users_endpoint = current_app.config['ENDPOINTS']['users']
    users = ServiceClient(users_endpoint)

    success, status_code, user, message = users.post('/users/check-identity', data)
    if success:
        access_token = create_access_token(identity={k: user[k] for k in ['guid', 'email', 'first_name', 'last_name']})

        return jsonify(dict(data=access_token)), status_code
    else:
        return jsonify(dict(data=data, message=message)), status_code
