import redis
import pymongo
from data_structure.cached import Cached


class RedisConnection(metaclass=Cached):
    def __init__(self, host, port, db, password):
        self.connection = redis.Redis(host, port, db, password)


class MongoConnection(metaclass=Cached):
    def __init__(self, host, port, db, user, password):
        conn = pymongo.MongoClient(host, port)
        db_eval_str = "conn.{}".format(db)
        database = eval(db_eval_str)
        auth_ret = database.authenticate(user, password, db)
        if not auth_ret:
            self.connection = False
        else:
            self.connection = database


class ConnectionFactory(object):
    @staticmethod
    def get_redis_connection(host='127.0.0.1', port=6379, db=0, password=''):
        redis_cached = RedisConnection(host, port, db, password)
        return redis_cached

    @staticmethod
    def get_mongo_connection(host='127.0.0.1', port=27017, db='', user='', password=''):
        mongo_cached = MongoConnection(host, port, db, user, password)
        return mongo_cached