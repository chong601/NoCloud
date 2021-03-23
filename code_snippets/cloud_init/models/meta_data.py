from abc import ABC
from uuid import uuid4, UUID
from .base_generator import BaseGenerator


class MetaDataGenerator(BaseGenerator, ABC):

    def __init__(self, uuid=None):
        self.uuid = uuid4() if uuid is None else UUID(uuid)

    def print_meta_data(self):
        template = super().j2_env.get_template('meta-data')
        print(template.render(instance_uuid=self.uuid))
