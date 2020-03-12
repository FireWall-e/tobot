#!/usr/bin/env python3
import time
# Библиотеки для работы с сервером
from http.server import HTTPServer
from server.main import Server
# Системные библиотеки
import os
import sys

HOST_NAME = '127.0.0.1' # Альтернатива localhost
PORT_NUMBER = 80 # Порт

if __name__ == '__main__':
    os.chdir(sys.path[0]) # Определяем корневую директорию проекта
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER)) # Логаем время запуска сервера
    try:
        httpd.serve_forever() # Запускаем сервер
    except KeyboardInterrupt: # При нажатии CTRL + C закрываем соединение с сервером и логаем
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))