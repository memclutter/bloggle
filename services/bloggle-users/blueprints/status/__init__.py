import datetime
from flask import Blueprint, jsonify, current_app

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def status():
    return jsonify({
        'success': True,
        'time': str(datetime.datetime.now()),
        'current_app': {
            'debug': current_app.debug,
            'testing': current_app.testing,
        },
    })
