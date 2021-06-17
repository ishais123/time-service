from flask import Flask
from datetime import datetime
import json

HEALTH_CHECK = {"Status": "healthy"}


app = Flask(__name__)

# HTTP listener
@app.route('/api/v1/time', methods=['POST', 'GET'])
def time_printer():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@app.route('/api/v1/health', methods=['POST', 'GET'])
def health():
    return json.dumps(HEALTH_CHECK), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8082)