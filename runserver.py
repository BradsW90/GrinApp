"""
This script runs the GrinApp application using a development server.
"""
import sys
from os import environ
import threading
from GrinApp import app
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
"""
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
        app.debug = False
    except ValueError:
        PORT = 5555
        app.debug = False
    app.run(HOST, PORT, threading=True)
"""

if __name__ =='__main__':
    #reload(sys)
    #sys.setdefaultencoding('UTF8')

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5113)
    IOLoop.instance().start()
