import datetime
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'success': True,
        'time': str(datetime.datetime.now())
    })
