import libvirt
from xml.etree import ElementTree

# String definitions


# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
POOL_TYPE = 'dir'
POOL_NAME = 'vm-ubuntu-focal-lxd-4'
TARGET_PATH = '/zfs-storage-test/kvm-area/vm-ubuntu-focal-lxd-4'

# Internal definitions
POOL_AUTOSTART = 1

libvirt_conn = libvirt.open(LIBVIRT_URI)

# XML GENERATION TIME *shudders*
pool_attr = {'type': POOL_TYPE}
pool_root = ElementTree.Element('pool', pool_attr)
pool_name = ElementTree.SubElement(pool_root, 'name').text = POOL_NAME
pool_target = ElementTree.SubElement(pool_root, 'target')
pool_target_path = ElementTree.SubElement(pool_target, 'path').text = TARGET_PATH

pool_xml = ElementTree.tostring(pool_root, 'unicode')
print(pool_xml)
libvirt_conn.storagePoolDefineXML(pool_xml)
pool_obj = libvirt_conn.storagePoolLookupByName(POOL_NAME)
pool_obj.setAutostart(POOL_AUTOSTART)
