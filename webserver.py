#!/usr/bin/python3
import datetime
import hashlib
import http.server
import os
import socket
import socketserver
from http import HTTPStatus

import psutil
from num2words import num2words

from settings import HASH_ITERATIONS

LISTENING_PORT = int(os.getenv('PYTHON_PORT', 8000))


def get_hex_red(cpu_percent):
    return hex(min(int((cpu_percent/100)*512), 255))[-2:]


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        current_time = str(datetime.datetime.now())
        iterations_text = num2words(HASH_ITERATIONS)
        hash_result = current_time
        for i in range(HASH_ITERATIONS):
            hash_result = hashlib.sha512(hash_result.encode('utf-8')).hexdigest()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        cpu_hex_red = get_hex_red(cpu_percent)
        memory_hex_red = get_hex_red(memory_percent)
        response = f"""<html><body>This message was sent from a machine
with name<br>
{socket.gethostname()}
<br><br>
listening on load balancer port<br>
{os.getenv('lowest_available_port')}
<br><br>
with actions run id<br>
{os.getenv('GITHUB_RUN_ID')}
<br><br>
This backend is currently using <span style="color:#{cpu_hex_red}0000;">{cpu_percent}%</span> of CPU and <span style="color:#{memory_hex_red}0000;">{memory_percent}%</span> of RAM.
<br>
I have made an expensive computation for you. The current date and time is {current_time} (or so it was, right before I started computing hashes).
If we hash this {HASH_ITERATIONS} ({iterations_text}) times with SHA512, we get 
<br><br>
{hash_result}</html></body>"""
        response_bytes = response.encode('utf-8')
        self.wfile.write(response_bytes)


httpd = socketserver.TCPServer(('0.0.0.0', LISTENING_PORT), Handler)
httpd.serve_forever()