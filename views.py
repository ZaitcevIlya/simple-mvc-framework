# V from MVT Pattern
from pprint import pprint

from simple_mvc_framework.templates_renderer import render
from patterns.creation_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, routes, Debug

site = Engine()
logger = Logger('main')


@AppRoute(routes=routes, url='/')
class IndexView:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/contact/')
class ContactView:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html')


@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html')


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Request for courses list')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('recorded', name, category)
                site.courses.append(course)

            logger.log(f'New course created')
            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None

            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            logger.log(f'New category created')
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Request for categories list')
        return '200 OK', render('category-list.html', objects_list=site.categories)


# @AppRoute(routes=routes, url='/copy-course/')
# class CopyCourse:
#     def __call__(self, request):
#         pprint(request)
#         request_params = request['request_params']
#
#         try:
#             name = request_params['name']
#             old_course = site.get_course(name)
#
#             if old_course:
#                 new_name = f'copy_{name}'
#                 new_course = old_course.clone()
#                 new_course.name = new_name
#                 site.courses.append(new_course)
#
#             return '200 OK', render('course-list.html',
#                                     objects_list=site.courses,
#                                     name=new_course.category.name)
#         except KeyError:
#             return '200 OK', 'No courses have been added yet'
