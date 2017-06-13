import unittest
from core.connection_factory import ConnectionFactory


class TestConnectionFactory(unittest.TestCase):
    def test_get_redis_connection(self):
        conn1 = ConnectionFactory.get_redis_connection(host='192.168.8.30')
        conn2 = ConnectionFactory.get_redis_connection(host='192.168.8.30')
        self.assertEqual(conn1, conn2)
        self.assertEqual(id(conn1.connection), id(conn2.connection))

    def test_get_mongo_connection(self):
        conn1 = ConnectionFactory.get_mongo_connection(host='192.168.8.28', db='d_weixin_robot', user='liliang', password='rock')
        conn2 = ConnectionFactory.get_mongo_connection(host='192.168.8.28', db='d_weixin_robot', user='liliang', password='rock')
        self.assertEqual(conn1, conn2)
        self.assertEqual(id(conn1.connection), id(conn2.connection))


if __name__ == '__main__':
    unittest.main()