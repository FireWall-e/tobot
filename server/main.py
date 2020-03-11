from http.server import BaseHTTPRequestHandler
from server.request.main import RequestHandler

class Server(BaseHTTPRequestHandler):
  # Инициализируем обработчик запросов
  requestHandler = RequestHandler()

  # Нижеприведенные методы с приставкой do_ автоматически вызываются при соответствующем типе запроса
  # Например, если на сервер поступил GET запрос, то вызовется функция do_GET, аналогично для остальных
  # https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/

  # Обработчик HEAD запросов
  def do_HEAD(self):
    # Обрабатываем запрос передавая запрашиваемый путь, например, для ссылки вида localhost/todo?id=123456789
    # запрашиваемым путем будет - /todo?id=123456789, а параметром - id со значением 123456789
    self.requestHandler.proceedRequest(requestPath = self.path)
    # Отправляем заголовки клиенту
    self.send_response(self.requestHandler.status)
    # Отправляем заголовок типа возвращаемого контента
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
    self.send_header("Content-type", self.requestHandler.contentType)
    # Сообщаем, что все заголовки необходимые заголовки переданы
    self.end_headers()
  
  # Обработчик GET запросов
  def do_GET(self):
    # Обрабатываем запрос и записываем полученные данные в переменную
    responseContentBytes = self.requestHandler.proceedRequest(requestPath = self.path)
    # Передаем данные в функцию, которая непосредственно отдает данные клиенту
    self.respond(responseContentBytes)
  
  # Обработчик POST запросов
  def do_POST(self):
    # Библиотека cgi необходима для получения тела POST запроса от клиента
    import cgi
    # Обрабатываем запрос, передавая запрашиваемый путь, 
    # относительный адрес от которой пришел запрос (например, для localhost - это '/')
    # и непосредственно сами данные postData, полученные при вызове cgi метода FieldStorage
    # о его аргументах можно прочесть в соотв. документации
    responseContentBytes = self.requestHandler.proceedRequest(
      requestPath = self.path,
      refererHeader = self.headers['Referer'],
      postData = cgi.FieldStorage(
        fp = self.rfile, 
        headers = self.headers,
        environ = {
          'REQUEST_METHOD': 'POST',
          'CONTENT_TYPE': self.headers['Content-Type']
        }
      )
    )
    # Передаем данные в функцию, которая непосредственно отдает данные клиенту
    self.respond(responseContentBytes)
  
  # Функция, которая отдает клиенту заголовки и обработанные сервером данные
  def respond(self, responseContentBytes):
    # Отдаем заголовки
    self.send_response(self.requestHandler.status)
    self.send_header("Content-type", self.requestHandler.contentType)
    self.end_headers()
    # Отдаем данные
    self.wfile.write(responseContentBytes)