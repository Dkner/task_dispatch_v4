import json
import logging
import asyncio
import aiohttp
from core.lcurl import Lcurl
from core.connection_factory import ConnectionFactory

logger = logging.getLogger(__name__)


class Worker(object):
    def __init__(self):
        self._loop = None

    def run(self):
        try:
            logger.warning('worker run...')
            self._loop = asyncio.new_event_loop()
            asyncio.ensure_future(coro_or_future=self.do_job(), loop=self._loop)
            self._loop.run_forever()
        except Exception as e:
            logger.error(e)
            asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        finally:
            self._loop.close()

    async def do_job(self):
        redis = ConnectionFactory.get_redis_connection()
        while True:
            task = redis.connection.rpop('test_task_list')
            if task is None:
                await asyncio.sleep(1)
                continue
            await self.run_task_api(task.decode())

    async def run_task_api(self, task_json_str):
        logger.warning('run task api: {}'.format(task_json_str))
        async with aiohttp.ClientSession(loop=self._loop) as session:
            ret = await Lcurl.post_json(session=session, url='http://127.0.0.1:5000/run_task',
                                        json=json.loads(task_json_str), headers={'Content': 'application/json'})
            logger.warning('task result: {}'.format(ret))
            redis = ConnectionFactory.get_redis_connection()
            redis.connection.lpush('test_task_result_list', task_json_str)


# if __name__ == '__main__':
#     from multiprocessing import Process
#     worker = Worker()
#     worker_process = Process(target=worker.run)
#     worker_process.start()
#     worker_process.join()