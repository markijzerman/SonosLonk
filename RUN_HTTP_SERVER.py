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

httpserverport1 = 8001
httpserverport2 = 8002
httpserverport3 = 8003
httpserverport4 = 8004
httpserverport5 = 8005

try:
    server1 = HttpServer(httpserverport1)
    server2 = HttpServer(httpserverport2)
    server3 = HttpServer(httpserverport3)
    server4 = HttpServer(httpserverport4)
    server5 = HttpServer(httpserverport5)
except:
    print("something went wrong trying to run servers!")
pass
    
print('starting httpservers')
server1.start()
server2.start()
server3.start()
server4.start()
server5.start()

try:
        while True:
            print('server running...')
            time.sleep(1)

except KeyboardInterrupt:
    server1.stop()
    server2.stop()
    server3.stop()
    server4.stop()
    server5.stop()
    
    pass
