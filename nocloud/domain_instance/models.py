from abc import ABC
from jinja2 import Environment, select_autoescape, PackageLoader


class BaseGenerator(object):

    # Quickly define our template stuff
    ENABLED_ESCAPES = ['html', 'xml']
    j2_env = Environment(
        # loader=FileSystemLoader('/home/chong601/PycharmProjects/pythonProject/templates/cloud-init'),
        loader=PackageLoader('code_snippets.templates', 'xmldef'),
        autoescape=select_autoescape(ENABLED_ESCAPES),
        trim_blocks=True,
        lstrip_blocks=True
    )

    def render(self):
        raise NotImplementedError('render() must be implemented')


class Domain(BaseGenerator, ABC):
    # domain_name, max_memory_unit, max_memory_amount,
    # provisioned_memory_unit, provisioned_memory_amount,
    # provisioned_vcpu_count, host_cpu_count,
    # cloud_init_nocloud_net_uri, cpu_mode, socket_count,
    # core_count, thread_count ,
    def __init__(self):
        pass

    def render(self):
        template = super().j2_env.get_template('centosdomainxmldef')
        print(template.render(vars(self)))


class CPU(object):

    def __init__(self, host_cpu_count: int, mode: str = None, socket_count: int = None, core_count: int = None,
                 thread_count: int = None):
        self.host_cpu_count = host_cpu_count if host_cpu_count is not None and host_cpu_count > 0 else ValueError(
            'Host CPU count must be more than zero!')
        self.mode = mode if mode is not None else 'host-model'
        self.socket_count = socket_count if socket_count is not None and socket_count > 0 else 1
        self.core_count = core_count if core_count is not None and core_count > 0 else self.host_cpu_count
        self.thread_count = thread_count if thread_count is not None and thread_count > 0 else 1

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def __repr__(self):
        return vars(self)


class Disk(object):

    def __init__(self, disk_type: str, disk_device: str, disk_driver_name: str, disk_driver_type: str,
                 disk_source_file: str, disk_target_device: str, disk_target_bus: str, disk_readonly: bool = None):
        self.disk_type = disk_type
        self.disk_device = disk_device
        self.disk_driver_name = disk_driver_name
        self.disk_driver_type = disk_driver_type
        self.disk_source_file = disk_source_file
        self.disk_target_device = disk_target_device
        self.disk_target_bus = disk_target_bus
        if disk_readonly is not None:
            self.disk_readonly = disk_readonly
        elif self.disk_device == 'cdrom':
            self.disk_readonly = True
        else:
            self.disk_readonly = False
