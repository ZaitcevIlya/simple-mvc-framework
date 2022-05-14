# Front Controller pattern and part of Page Controller

from datetime import date
from views import IndexView, ContactView


def some_front(request):
    request['some_front'] = 'some_front'


def today_date(request):
    request['date'] = date.today()


fronts = [some_front, today_date]

routes = {
    '/': IndexView(),
    '/contact/': ContactView()
}
