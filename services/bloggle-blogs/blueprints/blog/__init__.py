from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import IntegrityError, OperationalError

from blueprints.blog.models import Blog
from common import db

blog_blueprint = Blueprint('blog', __name__, url_prefix='/blogs')


@blog_blueprint.route('', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400
    
    user_guid = data.get('user_guid')
    title = data.get('title')
    about = data.get('about')
    
    try:
        blog = Blog(user_guid=user_guid,
                    title=title,
                    about=about)
        
        db.session.add(blog)
        db.session.commit()
    
        return jsonify({
            'success': True,
            'data': dict(blog),
        }), 201
    
    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@blog_blueprint.route('', methods=['GET'])
def index():
    try:
        return jsonify({
            'success': True,
            'data': [dict(u) for u in Blog.query.all()]
        }), 200
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@blog_blueprint.route('/<blog_guid>', methods=['PATCH'])
def update(blog_guid):
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    try:
        try:
            blog = Blog.query.filter_by(guid=blog_guid).first()
            if not blog:
                raise ValueError

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Blog (guid=%s) does not exist' % blog_guid
            }), 404

        blog.user_guid = data.get('user_guid', blog.user_guid)
        blog.title = data.get('title', blog.title)
        blog.about = data.get('about', blog.about)
        
        db.session.add(blog)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(blog),
        })

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@blog_blueprint.route('/<blog_guid>', methods=['GET'])
def view(blog_guid):
    try:
        blog = Blog.query.filter_by(guid=blog_guid).first()
        if not blog:
            raise ValueError

        return jsonify({
            'success': True,
            'data': dict(blog)
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Blog (guid=%s) does not exist' % blog_guid
        }), 404

    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@blog_blueprint.route('/<blog_guid>', methods=['DELETE'])
def delete(blog_guid):
    try:
        blog = Blog.query.filter_by(guid=blog_guid).first()
        if not blog:
            raise ValueError

        db.session.delete(blog)
        db.session.commit()

        return jsonify({
            'success': True,
        }), 204
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Blog (guid=%s) does not exist' % blog_guid
        }), 404

    except OperationalError as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500
