import json
import subprocess
from core.connection_factory import ConnectionFactory
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/run_task', methods=['POST'])
def run_task():
    task = request.get_json()
    ret_code = subprocess.call(task.get('script'))
    redis = ConnectionFactory.get_redis_connection()
    redis.connection.lpush(json.dumps(task))


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
