class Beat(object):
    def run(self):
        '''
        1）获取超过当前时间戳的需要触发的一批任务
        2）保存当前这批任务的状态信息，供任务完成时校对
        3）将这批任务的时间戳拨到下个触发点
        4）将这批任务推到broker
        :return:
        '''
        pass

    def fetch_job(self):
        '''
        获取超过当前时间戳的需要触发的一批任务
        :return:
        '''
        pass

    def update_trigger(self, job):
        '''
        根据job的类型，计算更新该job的下个触发点
        :param job:
        :return:
        '''
        pass

    def push_broker(self, task):
        '''
        将任务推到broker
        :param task:
        :return:
        '''
        pass