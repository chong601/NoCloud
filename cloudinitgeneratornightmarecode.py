import yaml

# Behold. The fuckery of Cloud-Init generator. Built using the "features" of PyYAML.
class CloudConfigNightmare(object):
    def __init__(self):
        # PLEASE NO TOUCHY _INTERNAL
        self._internal = {}

    def dump_as_yaml(self):
        # PyYAML doesn't support comments.
        # So I **forced** one inside here.
        # And because Cloud-Init **insists they need a comment in there.
        # Fuck Cloud-Init.
        return '#cloud-config\n{}'.format(yaml.safe_dump(self._internal))

    def add_property(self, another_dict):
        # Double stars because apparently Stack Overflow said It Works For Me:tm:
        # So I used it and It Works on My Machine Too:tm:
        self._internal.update(**another_dict)

    def delete_property(self, key):
        self._internal.pop(key)

    def print(self):
        print(self._internal)


# This is some drunken nightmare born from the hotness of Malaysian weather and because YAML library
# forced me to do this.
# Fuck YAML. Seriously.
ccn = CloudConfigNightmare()
ccn.add_property({'a': 'a'})
ccn.add_property({'b': 'b'})
ccn.add_property({'c': {'d': ['d', 'e', 'f']}})
print(ccn.dump_as_yaml())
