#!/usr/bin/env python3
import time
from http.server import HTTPServer
# import sys
# sys.path.insert(1, '/server')
from server.main import Server
import os
import sys

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 80

if __name__ == '__main__':
    # global ROOT 
    # ROOT = os.path.dirname(os.path.abspath(__file__))
    os.chdir(sys.path[0]) # Определяем корневую директорию проекта
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))