from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from common import ServiceClient

blog_blueprint = Blueprint('blog', __name__, url_prefix='/blogs')


@blog_blueprint.route('', methods=['POST'])
@jwt_required
def create():
    data = request.get_json()
    if not data:
        return jsonify(dict(success=False, message='Invalid payload'))

    current_user = get_jwt_identity()
    data['user_guid'] = current_user.get('guid')

    blogs_endpoint = current_app.config['ENDPOINTS']['blogs']
    blogs = ServiceClient(blogs_endpoint)

    success, status_code, data, message = blogs.post('/blogs', data)

    if success:
        return jsonify(data), status_code
    else:
        return jsonify(message=message, data=data), status_code


@blog_blueprint.route('', methods=['GET'])
@jwt_required
def index():
    data = dict(request.args)

    blogs_endpoint = current_app.config['ENDPOINTS']['blogs']
    blogs = ServiceClient(blogs_endpoint)

    success, status_code, data, message = blogs.get('/blogs', data)

    if success:
        return jsonify(data), status_code
    else:
        return jsonify(message=message, data=data), status_code


@blog_blueprint.route('/my', methods=['GET'])
@jwt_required
def index_my():
    data = dict(request.args)

    current_user = get_jwt_identity()
    data['user_guid'] = current_user.get('guid')
    blogs_endpoint = current_app.config['ENDPOINTS']['blogs']
    blogs = ServiceClient(blogs_endpoint)

    success, status_code, data, message = blogs.get('/blogs', data)

    if success:
        return jsonify(data), status_code
    else:
        return jsonify(message=message, data=data), status_code
