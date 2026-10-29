import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from app.main import Handler


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_health(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port)
        conn.request('GET', '/healthz')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.read())['status'], 'ok')
        conn.close()

    def test_readiness(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port)
        conn.request('GET', '/readyz')
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.read())['ready'], True)
        conn.close()

    def test_never_process_payments(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port)
        conn.request('POST', '/payments', body='{}')
        response = conn.getresponse()
        self.assertEqual(response.status, 405)
        self.assertIn('no payments', json.loads(response.read())['error'])
        conn.close()

if __name__ == '__main__':
    unittest.main()
