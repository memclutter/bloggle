import datetime
from flask import Blueprint, jsonify

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def status():
    return jsonify({
        'success': True,
        'time': str(datetime.datetime.now())
    })
