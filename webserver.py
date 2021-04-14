#!/usr/bin/python3
import http.server
import socketserver
import socket
from http import HTTPStatus
import os
import psutil
import datetime
import hashlib
from num2words import num2words

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        current_time=str(datetime.datetime.now())
        iterations=5000000
        iterations_text=num2words(iterations)
        hash_result = current_time
        for i in range(iterations):
            hash_result = hashlib.sha512(hash_result.encode('utf-8')).hexdigest()
        response = f"""This message was sent from {socket.gethostname()} with actions run id {os.getenv('GITHUB_RUN_ID')}
This backend is currently using {psutil.cpu_percent()}% of CPU and {psutil.virtual_memory().percent}% of RAM.

Here, I have made an expensive computation for you. The current date and time is {current_time} (or so it was, right before I started computing hashes).
If we hash this {iterations} ({iterations_text}) times with SHA512, we get {hash_result}"""
        response_bytes = response.encode('utf-8')
        self.wfile.write(response_bytes)


httpd = socketserver.TCPServer(('0.0.0.0', 8001), Handler)
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
