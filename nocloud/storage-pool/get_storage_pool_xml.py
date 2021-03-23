import libvirt
from xml.etree import ElementTree

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-1'

# Internal definitions


libvirt_conn = libvirt.open(LIBVIRT_URI)

pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
xml_data = pool.XMLDesc()

print(xml_data)

