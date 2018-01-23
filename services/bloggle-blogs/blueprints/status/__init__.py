import datetime
from flask import Blueprint, jsonify, current_app

status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/status', methods=['GET'])
def status():
    time = str(datetime.datetime.now())
    config_keys = ['DEBUG', 'TESTING']
    config = {k: v for (k, v) in current_app.config.items() if k in config_keys}

    return jsonify(dict(time=time, config=config)), 200
