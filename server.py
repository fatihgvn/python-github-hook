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

    def do_GET(self):
        print(self.headers)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("deneme server",'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode("utf-8"))

        repo = githubHook(data)

        if repo.event == repo.PAYLOAD:
            logger.info("create \"%s\" payload file" % (repo.payloadFile))
            with open(repo.payloadFile, 'w') as fp:
                json.dump(data, fp)
        elif repo.event == repo.PUSH:
            logger.info("Yeni bir pull isteği")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("deneme server",'utf-8'))


httpd = HTTPServer((HOST, PORT), Serv)
httpd.serve_forever()