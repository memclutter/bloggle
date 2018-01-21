from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from common import ServiceClient

user_blueprint = Blueprint('users', __name__, url_prefix='/users')


@user_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    current_user = get_jwt_identity()
    return jsonify(dict(success=True, data=current_user)), 200


@user_blueprint.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if not data:
        return jsonify(dict(success=False, message='Invalid payload')), 400

    email = data.get('email')
    password = data.get('password')

    if (not email) or (not password):
        return jsonify(dict(success=False, message='Invalid payload')), 400

    users_endpoint = current_app.config['ENDPOINTS']['users']
    users_client = ServiceClient(users_endpoint)

    try:
        ok, users, message = users_client.get('/users', dict(email=email))
    except RuntimeError as e:
        return jsonify(dict(success=False, message=str(e))), 500

    if not ok or (len(users) == 0):
        return jsonify(dict(success=False, message='Wrong email or password')), 400

    user = users[0]

    try:
        path = '/users/%s/check-password' % user['guid']
        ok, result, message = users_client.post(path, dict(password=password))
    except RuntimeError as e:
        return jsonify(dict(success=False, message=str(e))), 500

    if not ok:
        return jsonify(dict(success=False, message='Wrong email or password')), 400

    access_token = create_access_token(identity={k: user[k] for k in ['guid', 'email', 'first_name', 'last_name']})

    return jsonify(dict(success=True, data=access_token)), 200
