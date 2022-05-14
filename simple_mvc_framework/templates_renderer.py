from jinja2 import Template


def render(template_name, **kwargs):
    print(template_name)
    with open(template_name, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)


if __name__ == '__main__':
    output_test = render('about.html', context={'name': 'Ilya'})
    print(output_test)
