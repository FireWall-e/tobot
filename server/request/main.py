## -*- coding: utf-8 -*-

from routes.main import Routes

class RequestHandler():
    # def __init__(self):
    # def __init__(self):
    #     super().__init__()
    # contentType = ""
    # contents = False
    config = {
        'char-encoding': 'UTF-8',
        'database': {
            # 'name': 
            # 'driver': 'sqlite',
            # 'url': 'sqlite:///database/tobot.db',
            'url': 'sqlite:///database/tobot.db'
        },
        'ajax': {
            'file-path': '/server/request/ajax/',
            'module-path': 'server.request.ajax.',
            'file-name': 'main'
        },
        'template': {
            'directory-path': '/templates/',
            'module-path': 'templates.py.'
        }
    }
#'template-path'
    requestConfig = {
        'public': {
            'html': {
                # 'path': '/templates/',
                'content-type': 'text/html'
            },
            'js': {
                # 'path': 'assets/js',
                'content-type': 'text/javascript'
            },
            'css': {
                # 'path': 'assets/css',
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

    # inrequestConfig = {
    #     'content-type': 'text/html',
    #     'template': '404.html'
    # }

    # def setStatus(self, status):
    #     self.status = status

    # def setContentType(self, contentType):
    #     self.contentType = contentType

    def doesFileExist(self, requestPath):
        from pathlib import Path
        return Path('.' + requestPath).is_file()

    def pathExtractExtension(self, path):
        import os
        from urllib.parse import urlparse
        # print('RECEIVED PATH  ', path)             #[0] - названия файла
        return os.path.splitext(urlparse(path).path)[1][1:] # skip dot

    def pathExtractParams(self, path):
        import urllib.parse as urlparse
        from urllib.parse import parse_qs
        
        return parse_qs(urlparse.urlparse(path).query)

    def pathExtractBare(self, path):
        import urllib.parse as urlparse

        return urlparse.urlparse(path).path

    def fileExtractName(self, filename):
        return filename.split('.')[0]

    

    # def fileExtractName(self, name):
    #     return return os.path.splitext()

    # def proceedPostRequest(self, form):
    #     data = self.dynamicImport(self.config['ajax']['module-path'] + requestFileName, 'Main')(self.requestConfig['private'])
    #     self.contentType = data['content-type']


    def proceedRequest(self, requestPath = False, refererHeader = False, postData = False):
        barePath = self.pathExtractBare(requestPath) # Trim request parameters
        requestExtension = self.pathExtractExtension(barePath)
        # print('!!!!REFERER!!!!', self.pathExtractBare(refererHeader))
        # print('refererHeader  is ', )
        # Forecast defaults
        # self.staticRequest = True
        self.status = 200
        
    
        # print('Wwwwww', self.doesFileExist('./assets/css/index.css'))
        # print('isVR requestPath is ', requestPath, 'requestExtension is ', requestExtension)
        # print('requestExtension and self.doesFileExist(requestPath)', requestExtension and self.doesFileExist(requestPath),
        # 'requestExtension in self.requestConfig.keys()', requestExtension in self.requestConfig['public'].keys()
        # )
        if ( requestExtension and self.doesFileExist(barePath) and 
             requestExtension in self.requestConfig['public'].keys()
           ):  # file request
            fileToRespond = barePath
            self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        elif barePath in Routes: # directory request
            fileToRespond = self.config['template']['directory-path'] + Routes[barePath]['template']

            # if not self.doesFileExist(fileToRespond):
            #     fileToRespond = self.config['template-path'] + Routes['page-in-progress']['template']
            requestExtension =  self.pathExtractExtension(fileToRespond)

            if requestExtension == 'py':
                '''
                Заголовки будут определяться самим включенным файлом
                '''
                from functions.main import dynamicImport, findProperty
                # self.staticRequest = False
                requestFileName = self.fileExtractName(Routes[barePath]['template'])
           
                if requestFileName == self.config['ajax']['file-name']:
                    # fileToRespond = self.config['ajax']['ajax-path'] + Routes[requestPath]['template']
                    self.contentType = self.requestConfig['private']['json']['content-type']
                    kwargs = {
                        'postData': postData,
                        'handlerFilename': findProperty(Routes, [self.pathExtractBare(refererHeader), 'name'], True) or 'default',
                        'dynamicImportModule': dynamicImport,
                        'dbConfig': self.config['database']
                    }
                    # data = dynamicImport(self.config['ajax']['module-path'] + requestFileName, 'Main') \
                    # (postData, handlerFilename = findProperty(Routes, [self.pathExtractBare(refererHeader), 'name'], True) or 'default', dynamicImportModule = dynamicImport)
                    data = dynamicImport(self.config['ajax']['module-path'] + requestFileName, 'Main')(**kwargs)
                    # self.contentType = data['content-type']
                    # data = getattr(data, 'init')
                    # print('^^^^^^^^^^^^^^^^^^^^^^^^')
                else:
                    # fileToRespond = self.config['template']['directory-path'] + Routes[requestPath]['template']
                    self.contentType = self.requestConfig['private'][requestExtension]['content-type']
                    kwargs = {
                        'requestParams': self.pathExtractParams(requestPath),
                        'dbConfig': self.config['database']
                    }
                    data = dynamicImport(self.config['template']['module-path'] + requestFileName, 'Main')(**kwargs)
                    
                    # data = 'awdawd'
                # print('############', data)
                # wow.kek(wow)

                # Тут нужно динамично подключить файл, и засетить контент заголовок
                return bytes(data, self.config['char-encoding'])
            else: # ассетсы или html
                self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        else: # invalid request
            # print('REQUEST IS FALSE ')
            self.status = 404
            fileToRespond = self.config['template']['directory-path'] + Routes['404']['template']
            requestExtension =  self.pathExtractExtension(fileToRespond)
            self.contentType = self.requestConfig['public'][requestExtension]['content-type']
        # Static include
        with open(fileToRespond[1:], 'rb') as file:
            return bytes(file.read())
        




    # def getContents(self):
    #     return self.contents

    # def getStatus(self):
    #     return self.status

    # def getContentType(self):
    #     return self.contentType