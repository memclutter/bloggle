from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import IntegrityError, OperationalError

from blueprints.post.models import Post
from common import db

post_blueprint = Blueprint('post', __name__, url_prefix='/posts')


@post_blueprint.route('', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    blog_guid = data.get('blog_guid')
    title = data.get('title')
    about = data.get('about')

    try:
        post = Post(blog_guid=blog_guid,
                    title=title,
                    about=about)

        db.session.add(post)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(post),
        }), 201

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@post_blueprint.route('', methods=['GET'])
def index():
    try:
        return jsonify({
            'success': True,
            'data': [dict(u) for u in Post.query.all()]
        }), 200
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@post_blueprint.route('/<post_guid>', methods=['PATCH'])
def update(post_guid):
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    try:
        try:
            post = Post.query.filter_by(guid=post_guid).first()
            if not post:
                raise ValueError

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Post (guid=%s) does not exist' % post_guid
            }), 404

        post.blog_guid = data.get('blog_guid', post.blog_guid)
        post.title = data.get('title', post.title)
        post.about = data.get('about', post.about)

        db.session.add(post)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(post),
        })

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@post_blueprint.route('/<post_guid>', methods=['GET'])
def view(post_guid):
    try:
        post = Post.query.filter_by(guid=post_guid).first()
        if not post:
            raise ValueError

        return jsonify({
            'success': True,
            'data': dict(post)
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Post (guid=%s) does not exist' % post_guid
        }), 404

    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@post_blueprint.route('/<post_guid>', methods=['DELETE'])
def delete(post_guid):
    try:
        post = Post.query.filter_by(guid=post_guid).first()
        if not post:
            raise ValueError

        db.session.delete(post)
        db.session.commit()

        return jsonify({
            'success': True,
        }), 204
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Post (guid=%s) does not exist' % post_guid
        }), 404

    except OperationalError as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500
