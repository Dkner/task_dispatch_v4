import unittest
from core.connection_factory import ConnectionFactory


class TestConnectionFactory(unittest.TestCase):
    def test_get_redis_connection(self):
        conn1 = ConnectionFactory.get_redis_connection(host='192.168.8.30')
        conn2 = ConnectionFactory.get_redis_connection(host='192.168.8.30')
        self.assertEqual(id(conn1), id(conn2))
        self.assertEqual(id(conn1.connection), id(conn2.connection))


if __name__ == '__main__':
    unittest.main()