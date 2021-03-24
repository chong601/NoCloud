import libvirt
from xml.etree import ElementTree

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
XML_POOL_PATH = './target'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-3'

# Internal definitions

libvirt_conn = libvirt.open(LIBVIRT_URI)

# Fuck you, fuck you, fuck you, fuck you, fuck you and fuck you libvirt.
pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
xml = ElementTree.fromstring(pool.XMLDesc())
disks = xml.findall(XML_POOL_PATH)
print(disks[0].find('path').text)