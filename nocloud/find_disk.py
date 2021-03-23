import libvirt
from xml.etree import ElementTree
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# Parameters
DOMAIN_NAME = 'vm-ubuntu-focal-lxd-1'

# Internal definition
XML_DISK_PATH = './devices/disk'

domain = client.lookupByName(DOMAIN_NAME)
xml = ElementTree.fromstring(domain.XMLDesc())
disks = xml.findall(XML_DISK_PATH)

for disk in disks:
    if 'file' in disk.find("source").attrib:
        source = disk.find("source").attrib['file']
    else:
        source = 'n/a'
    target = disk.find("target").attrib['dev']
    print("{} | {}".format(source, target))
