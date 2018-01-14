from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, OperationalError

from blueprints.user.models import User
from common import db

user_blueprint = Blueprint('user', __name__, url_prefix='/users')


@user_blueprint.route('', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    try:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(user),
        }), 201

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@user_blueprint.route('', methods=['GET'])
def index():
    try:
        conditions = []

        if 'email' in request.args:
            conditions.append(User.email == request.args['email'])

        if 'first_name' in request.args:
            conditions.append(User.first_name.ilike(request.args['first_name']))

        if 'last_name' in request.args:
            conditions.append(User.first_name.ilike(request.args['last_name']))

        return jsonify({
            'success': True,
            'data': [dict(u) for u in User.query.filter(and_(*conditions)).all()]
        }), 200
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@user_blueprint.route('/<user_guid>', methods=['PATCH'])
def update(user_guid):
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload',
        }), 400

    try:
        try:
            user = User.query.filter_by(guid=user_guid).first()
            if not user:
                raise ValueError

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'User (guid=%s) does not exist' % user_guid
            }), 404

        user.email = data.get('email', user.email)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        if ('password' in data) and (len(data['password']) != 0):
            user.set_password(data.get('password'))

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': dict(user),
        })

    except (IntegrityError, OperationalError) as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@user_blueprint.route('/<user_guid>', methods=['GET'])
def view(user_guid):
    try:
        user = User.query.filter_by(guid=user_guid).first()
        if not user:
            raise ValueError

        return jsonify({
            'success': True,
            'data': dict(user)
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'User (guid=%s) does not exist' % user_guid
        }), 404

    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@user_blueprint.route('/<user_guid>', methods=['DELETE'])
def delete(user_guid):
    try:
        user = User.query.filter_by(guid=user_guid).first()
        if not user:
            raise ValueError

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
        }), 204
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'User (guid=%s) does not exist' % user_guid
        }), 404

    except OperationalError as e:
        db.session.rollback()

        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500


@user_blueprint.route('/<user_guid>/check_password', methods=['POST'])
def check_password(user_guid):
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Invalid payload'
        }), 400

    password = data.get('password')
    if not password:
        return jsonify({
            'success': False,
            'message': 'Missing password',
        }), 400

    try:
        try:
            user = User.query.filter_by(guid=user_guid).first()
            if not user:
                raise ValueError

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'User (guid=%s) does not exist' % user_guid
            })

        if user.check_password(password):
            return jsonify({
                'success': True
            }), 200
        else:
            return jsonify({
                'success': False,
            }), 400
    except OperationalError as e:
        message = 'Database error: %s' % e if current_app.debug else 'Server error'

        return jsonify({
            'success': False,
            'message': message,
        }), 500
