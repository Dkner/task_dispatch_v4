import json
import requests
from core.connection_factory import ConnectionFactory


class Worker(object):
    def run(self):
        redis = ConnectionFactory.get_redis_connection()
        while True:
            task = redis.connection.brpop('test_task_list')
            requests.post('http://127.0.0.1/run_task', json=task)
