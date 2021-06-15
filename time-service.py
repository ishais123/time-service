import time
from flask import Flask
from datetime import datetime


app = Flask(__name__)

# HTTP listener
@app.route('/api/v1/time', methods=['POST', 'GET'])
def time_printer():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8082)