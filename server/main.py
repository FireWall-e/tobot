from http.server import BaseHTTPRequestHandler
# from pathlib import Path
# from routes.main import Routes
from server.request.main import RequestHandler

class Server(BaseHTTPRequestHandler):
  requestHandler = RequestHandler()

  def do_HEAD(self):
    # https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/HEAD
    self.requestHandler.proceedRequest(requestPath = self.path)
    self.send_response(self.requestHandler.status)
    self.send_header("Content-type", self.requestHandler.contentType)
    self.end_headers()
    
  def do_GET(self):
 
    # valid_request = self.RH.isValidRequest(self.path)
 
    # print('valid request is ', valid_request)
    # print('COMMAND IS ', self.command)
    # file_extension = 
    # print('file extension is ', file_extension)
    # print('.headers.get is ', self.headers)
    responseContentBytes = self.requestHandler.proceedRequest(requestPath = self.path)
    self.send_response(self.requestHandler.status)
    self.send_header("Content-type", self.requestHandler.contentType)
    self.end_headers()
    self.respond(responseContentBytes)
    
  def do_POST(self):
    import cgi
    # content_len = int(self.headers.get('Content-Length'))
    # post_body = self.rfile.read(content_len)
    # form = cgi.FieldStorage(
    #   fp = self.rfile, 
    #   headers = self.headers,
    #   environ = {
    #     'REQUEST_METHOD':'POST',
    #     'CONTENT_TYPE':self.headers['Content-Type']
    #   }
    # )
    print('HEADERS ARE', self.headers)
    print('CONTENT TYPE RECEIVED',  self.headers['Content-Type'])
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
    # print( form, form.getvalue('test'))
    self.respond(responseContentBytes)
    
  # def handle_http(self):
  #   self.send_response(self.requestHandler.status)
  #   self.send_header('Content-type', self.requestHandler.contentType)
  #   self.end_headers()
  #   response_content = open(self.requestHandler.fileToRespond[1:]).read()

  #   print('response content is ', response_content)
  #   return bytes(response_content, 'UTF-8')
    
  def respond(self, responseContentBytes):
    # content = self.handle_http()
    self.wfile.write(responseContentBytes)
    # self.wfile.close()