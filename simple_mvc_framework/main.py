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

    def content_type(self, path):
        if path.endswith(".css"):
            return "text/css"
        # elif path.endswith(".png"):
        #     return "image/png"
        else:
            return "text/html"
