from abc import ABC
from passlib.hash import sha512_crypt
from .base_generator import BaseGenerator


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
