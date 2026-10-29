"""Mock API for infrastructure testing only. No real payments or data storage."""
import json
import logging
import os
import signal
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logging.basicConfig(level=logging.INFO, format='%(message)s')
STARTED = time.time()

class Handler(BaseHTTPRequestHandler):
    server_version = 'MockPaymentAPI/0.1'

    def log_message(self, format_, *args):
        logging.info(json.dumps({'event': 'access', 'client': self.client_address[0],
                                 'message': format_ % args}))

    def _json(self, status, obj):
        payload = json.dumps(obj, sort_keys=True).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == '/healthz':
            return self._json(200, {'status': 'ok'})
        if self.path == '/readyz':
            return self._json(200, {'ready': True})
        if self.path == '/api/v1/info':
            return self._json(200, {'service': 'mock-payment-api', 'simulation': True,
                                    'warning': 'No actual payment processing'})
        if self.path == '/metrics':
            payload = (f'# HELP app_uptime_seconds Process uptime in seconds\n'
                       '# TYPE app_uptime_seconds gauge\n'
                       f'app_uptime_seconds {int(time.time() - STARTED)}\n').encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            return self.wfile.write(payload)
        return self._json(404, {'error': 'not found'})

    def do_POST(self):
        # Intentionally no payment or customer endpoints: infrastructure demo only.
        return self._json(405, {'error': 'no payments are accepted by this mock service'})


def serve(port=8080):
    server = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    def shutdown(signum, frame):
        logging.info(json.dumps({'event': 'shutdown', 'signal': signum}))
        threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    logging.info(json.dumps({'event': 'listening', 'port': port}))
    try:
        server.serve_forever()
    finally:
        server.server_close()

if __name__ == '__main__':
    serve(int(os.environ.get('PORT', '8080')))
