# V from MVT Pattern

from simple_mvc_framework.templates_renderer import render


class IndexView:
    def __call__(self, request):
        return '200 OK', render(f'./templates/index.html', date=request.get('date', None))


class ContactView:
    def __call__(self, request):
        return '200 OK', render(f'./templates/contact.html')
