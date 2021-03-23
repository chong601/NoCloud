from jinja2 import FileSystemLoader, Environment, select_autoescape, PackageLoader


class BaseGenerator(object):

    # Quickly define our template stuff
    ENABLED_ESCAPES = ['html', 'xml']
    j2_env = Environment(
        # loader=FileSystemLoader('/home/chong601/PycharmProjects/pythonProject/templates/cloud-init'),
        loader=PackageLoader('code_snippets.templates', 'cloudinit'),
        autoescape=select_autoescape(ENABLED_ESCAPES),
        trim_blocks=True,
        lstrip_blocks=True
    )

    def render(self):
        raise NotImplementedError('render() must be implemented')
