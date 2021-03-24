from jinja2 import Environment, select_autoescape, PackageLoader
from abc import ABC
from uuid import uuid4, UUID
from passlib.handlers.sha2_crypt import sha512_crypt


class BaseGenerator(object):
    # Quickly define our template stuff
    ENABLED_ESCAPES = ['html', 'xml']
    j2_env = Environment(
        # loader=FileSystemLoader('/home/chong601/PycharmProjects/pythonProject/templates/cloud-init'),
        loader=PackageLoader('nocloud.templates', 'cloudinit'),
        autoescape=select_autoescape(ENABLED_ESCAPES),
        trim_blocks=True,
        lstrip_blocks=True
    )

    def render(self):
        raise NotImplementedError('render() must be implemented')


class MetaDataGenerator(BaseGenerator, ABC):

    def __init__(self, uuid=None):
        self.uuid = uuid4() if uuid is None else UUID(uuid)

    def render(self):
        template = super().j2_env.get_template('meta-data')
        print(template.render(instance_uuid=self.uuid))


class NetworkConfigGenerator(BaseGenerator, ABC):

    def __init__(self):
        pass

    def render(self):
        template = super().j2_env.get_template('network-config')
        print(template.render())


class UserDataGenerator(BaseGenerator, ABC):

    # TODO: complete user data generator code
    def __init__(self):
        pass
        # self.uuid = uuid4()

    def render(self):
        template = super().j2_env.get_template('user-data')
        print(template.render(instance_uuid=self.uuid))


class VendorDataGenerator(BaseGenerator, ABC):

    def __init__(self, password, hostname, require_update=True, require_upgrade=True, require_reboot=True):
        self.password = sha512_crypt.hash(password)
        self.hostname = hostname
        self.require_update = require_update
        self.require_upgrade = require_upgrade
        self.require_reboot = require_reboot

    def render(self):
        template = super().j2_env.get_template('vendor-data')
        print(template.render(random_password=self.password, hostname=self.hostname, require_update=self.require_update,
                              require_upgrade=self.require_upgrade, require_reboot=self.require_reboot))
