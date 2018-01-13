from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import IntegrityError, OperationalError

from blueprints.comment.models import Comment
from common import db

comment_blueprint = Blueprint('comment', __name__, url_prefix='/comments')


@comment_blueprint.route('', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    post_guid = data.get('post_guid')
    user_guid = data.get('user_guid')
    body = data.get('body')
    reply_to_guid = data.get('reply_to_guid')

    try:
        comment = Comment(post_guid=post_guid,
                          user_guid=user_guid,
                          body=body,
                          reply_to_guid=reply_to_guid)

        db.session.add(comment)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(comment),
        }), 201

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@comment_blueprint.route('', methods=['GET'])
def index():
    try:
        return jsonify({
            'success': True,
            'data': [dict(u) for u in Comment.query.all()]
        }), 200
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@comment_blueprint.route('/<comment_guid>', methods=['PATCH'])
def update(comment_guid):
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    try:
        try:
            comment = Comment.query.filter_by(guid=comment_guid).first()
            if not comment:
                raise ValueError

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Comment (guid=%s) does not exist' % comment_guid
            }), 404

        comment.post_guid = data.get('post_guid', comment.post_guid)
        comment.user_guid = data.get('user_guid', comment.user_guid)
        comment.body = data.get('body', comment.body)
        comment.reply_to_guid = data.get('about', comment.reply_to_guid)

        db.session.add(comment)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(comment),
        })

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@comment_blueprint.route('/<comment_guid>', methods=['GET'])
def view(comment_guid):
    try:
        comment = Comment.query.filter_by(guid=comment_guid).first()
        if not comment:
            raise ValueError

        return jsonify({
            'success': True,
            'data': dict(comment)
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Comment (guid=%s) does not exist' % comment_guid
        }), 404

    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@comment_blueprint.route('/<comment_guid>', methods=['DELETE'])
def delete(comment_guid):
    try:
        comment = Comment.query.filter_by(guid=comment_guid).first()
        if not comment:
            raise ValueError

        db.session.delete(comment)
        db.session.commit()

        return jsonify({
            'success': True,
        }), 204
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Comment (guid=%s) does not exist' % comment_guid
        }), 404

    except OperationalError as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500
