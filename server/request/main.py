## -*- coding: utf-8 -*-
# Содержит роуты всего сайта, т.е. конфиг с данными для какого запроса какой файл вызывать
from routes.main import Routes

# Собственно сам обработчик запросов
class RequestHandler():

    # Главная конфигурационная переменная
    config = {
        'char-encoding': 'UTF-8',
        'database': { # https://dataset.readthedocs.io/en/latest/index.html
            'url': 'sqlite:///database/tobot.db'
        },
        'ajax': { # Конфиг для ajax запросов
            'file-path': '/server/request/ajax/',
            'module-path': 'server.request.ajax.',
            'file-name': 'main'
        },
        'template': { # Конфиг с путями для шаблонов статический страниц (html) и страниц с данными сервера (модулями) (py)
            'directory-path': '/templates/',
            'module-path': 'templates.py.'
        }
    }

    # Конфиг запросов, содержащий обрабатываемые (разрешенные) сервером типы контента
    # public - доступны для прямого доступа через адресную строку
    # private - предварительно обрабатываются сервером
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
    requestConfig = {
        'public': {
            'html': {
                'content-type': 'text/html'
            },
            'js': {
                'content-type': 'text/javascript'
            },
            'css': {
                'content-type': 'text/css'
            },
            'png': {
                'content-type': 'image/png'
            },
            'jpg': {
                'content-type': 'image/jpeg'
            },
            'jpeg': {
                'content-type': 'image/jpeg'
            },
            'svg': {
                'content-type': 'image/svg+xml'
            },
            'gif': {
                'content-type': 'image/gif'
            }
        },
        'private': {
            'py': {
                'content-type': 'text/html'
            },
            'json': {
                'content-type': 'application/json'
            },
            'jsonp': {
                'content-type': 'application/javascript'
            }
        }
        
    }

    # Функция, которая проверяет существует ли файл по указанному пути requestPath,
    # точка сообщает, что путь от корня - tobot/
    def doesFileExist(self, requestPath):
        from pathlib import Path
        return Path('.' + requestPath).is_file()

    # Функция для получения расширения файла,
    # то есть для something.exe, вернет exe [1] (без точки [1:])
    def pathExtractExtension(self, path):
        import os
        from urllib.parse import urlparse
        
        return os.path.splitext(urlparse(path).path)[1][1:]


    # Возвращает параметры запроса типа dictionary,
    # т.е. для запроса localhost/todo?id=123456789
    # должно вернуть {'id': '123456789'}
    def pathExtractParams(self, path):
        import urllib.parse as urlparse
        from urllib.parse import parse_qs
        
        return parse_qs(urlparse.urlparse(path).query)

    # Извлекает "чистый" запрашиваемый путь из ссылки
    # Например,  для запроса localhost/todo?id=123456789
    # должна вернуть /todo
    def pathExtractBare(self, path):
        import urllib.parse as urlparse

        return urlparse.urlparse(path).path

    # Возвращает имя файла
    # Например, для something.exe вернет something
    def fileExtractName(self, filename):
        return filename.split('.')[0]

    # Функция обработки запроса
    def proceedRequest(self, requestPath = False, refererHeader = False, postData = False):
        # Извлекаем "чистый" путь запроса
        barePath = self.pathExtractBare(requestPath)
        # Получаем расширение запрашиваемого файла (если оно есть)
        requestExtension = self.pathExtractExtension(barePath)
        # Например, для localhost/assets/css/main.css получим
        # barePath - localhost/assets/css/main.css 
        # requestExtension - css
        ##########################################################

        # По дефолту выставляем код успешного ответа - 200
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        self.status = 200

        # Если запрашивается файл, то бишь есть запрашиваемое расширение и файл существует физически
        # а также является public (публично доступным)
        # то выполняется данное условие
        if ( requestExtension and self.doesFileExist(barePath) and 
             requestExtension in self.requestConfig['public'].keys()
           ):
            # В переменную возвращаемого файла записываем "чистый путь"
            # по которому сервер позже обратится за данными
            fileToRespond = barePath
            # Записываем соответствующий расширению тип контента
            self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        elif barePath in Routes: # Если запрашиваемый путь существует в роутах то выполняется условие
            # К конфигу с путем для шаблонов дописываем имя файла из конфига роутов
            # и получаем полноценный путь к файлу, к которому сервер позже обратится за данными
            fileToRespond = self.config['template']['directory-path'] + Routes[barePath]['template']
            # Вытаскиваем расширение по нашему ранее полученному пути fileToRespond
            requestExtension =  self.pathExtractExtension(fileToRespond)
            # Если это файлик питона с расширением .py, то
            if requestExtension == 'py':
                # Из функция текущего проекта импортируем одну для динамического импорта и одну для поиска
                # свойства в объекте со вложенностями
                from functions.main import dynamicImport, findProperty
                # Вытаскиваем имя файла без расширения
                requestFileName = self.fileExtractName(Routes[barePath]['template'])
                # Проверяем, если имя соответствует имени при AJAX POST запросе
                if requestFileName == self.config['ajax']['file-name']:
                    # Записываем приватные заголовки возвращаемого контанта
                    # Для AJAX запроса - это json строка с объектом
                    self.contentType = self.requestConfig['private']['json']['content-type']
                    # Для удобства создаем словарь аргументов функции
                    kwargs = {
                        'postData': postData, # Записываем данные полученные с cgi.FieldStorage
                        'handlerFilename': findProperty(Routes, [self.pathExtractBare(refererHeader), 'name'], True) or 'default', # Если в роутах указано имя файла (name) для обработки AJAX запросов, то присваиваем его, в противном случае файл обработки - default.py
                        'dynamicImportModule': dynamicImport, # Записываем модуль динамического импорта
                        'dbConfig': self.config['database'] # Передаем "ссылку" на БД https://dataset.readthedocs.io/en/latest/api.html#connecting
                    }
                    # Получаем данные из динамически подключаемого файла 
                    # (сразу же вызываем функцию Main внутри него) и передаем все аргументы kwargs
                    data = dynamicImport(self.config['ajax']['module-path'] + requestFileName, 'Main')(**kwargs)
                else:
                    # Записываем заголовки
                    self.contentType = self.requestConfig['private'][requestExtension]['content-type']
                    # Аргументы
                    kwargs = {
                        'requestParams': self.pathExtractParams(requestPath), # Передаем запрашиваемыу параметры типа dictionary (словарь)
                        'dbConfig': self.config['database']
                    }
                    data = dynamicImport(self.config['template']['module-path'] + requestFileName, 'Main')(**kwargs)
                # Возвращаем информацию в виде набора байтов с кодировкой (UTF-8)
                return bytes(data, self.config['char-encoding'])
            else: 
                # Заголовки статики (html, css, js, изображения и прочее)
                self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        else: 
            # Запрос не удалось обработать - 404 код ответа
            self.status = 404
            # Возвращаем страницу 404.html
            fileToRespond = self.config['template']['directory-path'] + Routes['404']['template']
            requestExtension =  self.pathExtractExtension(fileToRespond)
            self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        # Также возвращаем байты
        with open(fileToRespond[1:], 'rb') as file:
            return bytes(file.read())