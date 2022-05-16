from quopri import decodestring

from simple_mvc_framework.requests import GetRequests, PostRequests
from simple_mvc_framework.templates_renderer import render


class StaticFiles:
    """Render static files such as styles or images"""
    def __init__(self, file_path):
        self.file_path = file_path

    def __call__(self, request):
        return '200 OK', render(f'./{self.file_path}')


class PageNotFound:
    def __call__(self, request):
        return '404 NOT FOUND', render(f'./templates/404.html')


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        request = {}
        # Define request method
        method = env['REQUEST_METHOD']
        request['method'] = method
        # Process the request depending on its type
        if method == 'GET':
            request_params = GetRequests().get_request_params(env)
            request['request_params'] = Application.decode_value(request_params)
            print(f'We got GET-request:'
                  f' {Application.decode_value(request_params)}')
        if method == 'POST':
            data = PostRequests().get_request_params(env)
            request['data'] = Application.decode_value(data)
            print(f'We got POST-request: {Application.decode_value(data)}')

        # Render pages by routes
        if path in self.routes:
            view = self.routes[path]
        # Load static CSS files to apply styles
        elif path.endswith(".css"):
            view = StaticFiles(path)
        # TODO: add image support later
        # elif path.endswith(".css") or path.endswith(".png"):
        else:
            view = PageNotFound()

        for front in self.fronts:
            front(request)
        code, body = view(request)
        # add specific content type based on file extension
        start_response(code, [('Content-Type', self.content_type(path))])

        return [body.encode('utf-8')]

    @staticmethod
    def content_type(path):
        if path.endswith(".css"):
            return "text/css"
        # elif path.endswith(".png"):
        #     return "image/png"
        else:
            return "text/html"

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'utf-8')
            val_decode_str = decodestring(val).decode('utf-8')
            new_data[k] = val_decode_str
        return new_data
