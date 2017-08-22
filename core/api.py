import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/run_task', methods=['POST'])
def run_task():
    task = request.get_json()
    print('run task[{}]'.format(task.get('id')))
    ret_code = subprocess.call(task.get('script'))
    return jsonify({
        'code': 200,
        'msg': ret_code,
        'data': ''
    })


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
