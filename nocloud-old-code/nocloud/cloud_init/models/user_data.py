from abc import ABC
from .base_generator import BaseGenerator


class UserDataGenerator(BaseGenerator, ABC):

    def __init__(self):
        pass
        # self.uuid = uuid4()

    def render(self):
        template = super().j2_env.get_template('user-data')
        print(template.render(instance_uuid=self.uuid))
