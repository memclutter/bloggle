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
    user_guid = current_user.get('guid')

    title = data.get('title')
    about = data.get('about')

    errors = dict()

    if not title:
        errors['title'] = 'Title is required'

    if len(errors) > 0:
        return jsonify(dict(success=False, data=errors, message='Validation failed')), 422

    blogs_endpoint = current_app.config['ENDPOINTS']['blogs']
    blogs = ServiceClient(blogs_endpoint)

    try:
        ok, data, message = blogs.post('/blogs', dict(user_guid=user_guid, title=title, about=about))
    except RuntimeError as e:
        return jsonify(dict(success=False, message=str(e))), 500

    if not ok:
        return jsonify(dict(success=False, message=message)), 400

    return jsonify(dict(success=True, data=data)), 201
