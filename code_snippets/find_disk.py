import libvirt
from xml.etree import ElementTree
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

domain = client.lookupByName("vm-ubuntu-focal-lxd-1")
xml = ElementTree.fromstring(domain.XMLDesc())
disks = xml.findall("./devices/disk")

for disk in disks:
    if 'file' in disk.find("source").attrib:
        source = disk.find("source").attrib['file']
    else:
        source = 'n/a'
    target = disk.find("target").attrib['dev']
    print("{} | {}".format(source, target))
