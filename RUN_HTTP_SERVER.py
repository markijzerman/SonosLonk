#!/usr/bin/env python

import os
import sys
import time
import socket
import struct

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread

class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, port):
        super(HttpServer, self).__init__()
        self.daemon = True
        handler = SimpleHTTPRequestHandler
        self.httpd = TCPServer(("", port), handler)
        self.httpd.allow_reuse_address = True

    def run(self):
        """Start the server"""
        print('Start HTTP server')
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        self.httpd.socket.close()
        self.httpd.shutdown()
        self.httpd.server_close()
        print('Stop HTTP server')

httpserverport = 8000

server = HttpServer(httpserverport)
server.start()



try:
        while True:
            print('server running...')
            time.sleep(1)

except KeyboardInterrupt:
    server.stop()
    
    pass
