# Front Controller pattern and part of Page Controller

from datetime import date
from views import IndexView, ContactView, StudyPrograms, CoursesList, CreateCourse, \
    CreateCategory, CategoryList


def some_front(request):
    request['some_front'] = 'some_front'


def today_date(request):
    request['date'] = date.today()


fronts = [some_front, today_date]

routes = {
    '/': IndexView(),
    '/contact/': ContactView(),
    '/study-programs/': StudyPrograms(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList()
    # '/copy-course/': CopyCourse()
}
