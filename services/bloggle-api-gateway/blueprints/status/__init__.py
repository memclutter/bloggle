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
            status_of_services[name] = resp.json()
        except ValueError:
            status_of_services[name] = resp.text

    time = str(datetime.datetime.now())
    config_keys = ['DEBUG', 'TESTING']
    config = {k: v for (k, v) in current_app.config.items() if k in config_keys}

    return jsonify(dict(time=time, config=config, status_of_services=status_of_services)), 200
