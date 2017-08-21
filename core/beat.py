import logging
import time
import json
from models.task import TaskModel
from core.connection_factory import ConnectionFactory

logger = logging.getLogger(__name__)


class Beat(object):
    current_tasks = {}

    def run(self):
        '''
        1）获取超过当前时间戳的需要触发的一批任务
        2）保存当前这批任务的状态信息，供任务完成时校对
        3）将这批任务推到broker
        4）将这批任务的时间戳拨到下个触发点
        :return:
        '''
        tasks = self.fetch_job()
        self.push_broker(tasks)

    def fetch_job(self):
        '''
        获取超过当前时间戳的需要触发的一批任务
        :return:
        '''
        tasks = TaskModel.query_task_to_trigger()
        TaskModel.execute('update task set exec_status = 1 where trigger_time<{} and exec_status = 0'.format(int(time.time())))
        logger.info('fetch job...{}'.format(str(tasks)))
        return tasks

    def update_trigger(self, job):
        '''
        根据job的类型，计算更新该job的下个触发点
        :param job:
        :return:
        '''
        now = int(time.time())
        if job.interval_type == 1:
            TaskModel.execute('update task set exec_status=0, trigger_time={}, update_at={} where id = {}'.format(0, now, job.id))
        elif job.interval_type == 2:
            TaskModel.execute('update task set exec_status=3, update_at={} where id = {}'.format(now, job.id))
        elif job.interval_type == 3:
            TaskModel.execute('update task set exec_status=0, trigger_time={}, update_at={} where id = {}'.format(now+job.time_detail, now, job.id))

    def push_broker(self, tasks):
        '''
        将任务推到broker
        :param task:
        :return:
        '''
        redis = ConnectionFactory.get_redis_connection()
        for task in tasks:
            redis.connection.lpush('test_task_list', json.dumps(task.__dict__))

    def async_result(self):
        '''
        将队列中的任务执行结果回收，调用update trigger
        :return:
        '''
        redis = ConnectionFactory.get_redis_connection()
        while True:
            result = redis.connection.brpop('test_task_result_list')
            task = json.loads(result)
            self.update_trigger(task)