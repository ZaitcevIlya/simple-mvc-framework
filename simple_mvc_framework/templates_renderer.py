from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)

    # temporary solution for processing css files
    if not template_name.endswith('.css'):
        template = env.get_template(template_name)
    else:
        with open(template_name, encoding='utf-8') as f:
            template = Template(f.read())

    return template.render(**kwargs)


if __name__ == '__main__':
    output_test = render('about.html', context={'name': 'Ilya'})
    print(output_test)
