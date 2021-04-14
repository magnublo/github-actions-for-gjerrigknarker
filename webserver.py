#!/usr/bin/python3
import http.server
import socketserver
import socket
from http import HTTPStatus
import os


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        response = f"This message was sent from {socket.gethostname()} with actions run id {os.getenv('GITHUB_RUN_ID')}"
        response_bytes = response.encode('utf-8')
        self.wfile.write(response_bytes)


httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()


# python3 server.py
# 127.0.0.1 - - [11/Apr/2017 11:36:49] "GET / HTTP/1.1" 200 -
# http :8000
'''
HTTP/1.0 200 OK
Date: Tue, 11 Apr 2017 15:36:49 GMT
Server: SimpleHTTP/0.6 Python/3.5.2
Hello world
'''
