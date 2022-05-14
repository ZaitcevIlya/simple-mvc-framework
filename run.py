# Application runner

from wsgiref.simple_server import make_server

from simple_mvc_framework.main import Application
from urls import routes, fronts

framework = Application(routes, fronts)

if __name__ == '__main__':
    with make_server('', 8000, framework) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
