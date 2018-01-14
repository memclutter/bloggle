import datetime

import requests
from flask import Blueprint, jsonify, current_app

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def status():
    status_of_services = dict(blogs=None, comments=None, posts=None, users=None)
    for name, endpoint in current_app.config['ENDPOINTS'].items():
        resp = requests.get(endpoint + 'status')

        try:
            body = resp.json()
        except ValueError:
            body = {'success': False, 'message': resp.text}

        status_of_services[name] = {
            'status_code': resp.status_code,
            'body': body
        }

    return jsonify({
        'success': True,
        'time': str(datetime.datetime.now()),
        'current_app': {
            'debug': current_app.debug,
            'testing': current_app.testing,
        },
        'status_of_services': status_of_services,
    })
