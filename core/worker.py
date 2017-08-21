import json
import subprocess
from core.connection_factory import ConnectionFactory
from models.task import TaskModel


class Worker(object):
    def run(self):
        redis = ConnectionFactory.get_redis_connection()
        while True:
            task = redis.connection.brpop('test_task_list')
            task = json.loads(task)
            self.execute_script(task)

    def execute_script(self, task):
        subprocess.Popen(task.script)
