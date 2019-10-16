#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json 
from psutil import process_iter
from signal import SIGTERM # or SIGKILL
from logger import logger
from githubHook import githubHook

PORT = 8181
HOST = ""
# HOST = "165.22.83.111"

for proc in process_iter():
    for conns in proc.connections(kind='inet'):
        if conns.laddr.port == PORT:
            proc.send_signal(SIGTERM) # or SIGKILL

class Serv(BaseHTTPRequestHandler):
    timeout = 5

    def log_message(self, format, *args):
        with open('accessLog.log', 'a+') as f:
            f.write("%s - - [%s] %s\n" %
                            (self.client_address[0],
                             self.log_date_time_string(),
                             format%args))


    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("OK",'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode("utf-8"))

        repo = githubHook(data)

        if repo.event == repo.PAYLOAD:
            repo.addNewProject()
        elif repo.event == repo.PUSH:
            repo.pull()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("OK",'utf-8'))


httpd = HTTPServer((HOST, PORT), Serv)
httpd.serve_forever()