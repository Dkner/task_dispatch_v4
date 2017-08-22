import threading
import time
import json
from models.task import TaskModel
from core.connection_factory import ConnectionFactory
from utils.my_logger import get_logger

logger = get_logger(__name__)


class Beat(object):

    def run(self):
        logger.warning('beat run...')
        push_task_thread = threading.Thread(target=self.push_task, daemon=True)
        push_task_thread.start()
        async_result_thread = threading.Thread(target=self.async_result, daemon=True)
        async_result_thread.start()

        push_task_thread.join()
        async_result_thread.join()

    def push_task(self):
        '''
        1）获取超过当前时间戳的需要触发的一批任务
        2）将这批任务推到broker
        :return:
        '''
        while True:
            tasks = self.fetch_job()
            self.push_broker(tasks)
            time.sleep(5)

    def fetch_job(self):
        '''
        获取超过当前时间戳的需要触发的一批任务
        :return:
        '''
        tasks = TaskModel.query_task_to_trigger()
        if tasks:
            TaskModel.execute('update task set exec_status = 1 where trigger_time<{} and exec_status = 0'.format(int(time.time())))
        return tasks

    def update_trigger(self, job):
        '''
        根据job的类型，计算更新该job的下个触发点
        :param job:
        :return:
        '''
        # logger.warning('update trigger for job: {}'.format(str(job)))
        now = int(time.time())
        if job.get('interval_type') == 1:
            TaskModel.execute('update task set exec_status=0, trigger_time={}, update_at={} where id = {}'.format(0, now, job.get('id')))
        elif job.get('interval_type') == 2:
            TaskModel.execute('update task set exec_status=3, update_at={} where id = {}'.format(now, job.get('id')))
        elif job.get('interval_type') == 3:
            TaskModel.execute('update task set exec_status=0, trigger_time={}, update_at={} where id = {}'.format(now+job.get('time_detail', 0), now, job.get('id')))

    def push_broker(self, tasks):
        '''
        将任务推到broker
        :param task:
        :return:
        '''
        redis = ConnectionFactory.get_redis_connection()
        if tasks:
            for task in tasks:
                task.__dict__.pop('_sa_instance_state')
                redis.connection.lpush('test_task_list', json.dumps(task.__dict__))
            logger.warning('push tasks to broker: {}'.format(tasks))

    def async_result(self):
        '''
        将队列中的任务执行结果回收，调用update trigger
        :return:
        '''
        redis = ConnectionFactory.get_redis_connection()
        while True:
            result = redis.connection.brpop('test_task_result_list')
            task = json.loads(result[1].decode())
            logger.warning('async result...{}'.format(task.get('id')))
            self.update_trigger(task)


# if __name__ == '__main__':
#     from multiprocessing import Process
#     beat = Beat()
#     beat_process = Process(target=beat.run)
#     beat_process.start()
#     beat_process.join()