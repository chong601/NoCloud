import libvirt
from xml.etree import ElementTree
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# WARNING: This will break the device on the instance if the device is still in use
# ie. mounted as a filesystem. Probably offer this feature if the instance is shut down

# create XML definition
disk_attr = {'type': 'file'}
disk = ElementTree.Element('disk')

target_pool = client.storagePoolLookupByName('vm-ubuntu-focal-lxd-1')
target_vol = target_pool.storageVolLookupByName('disk-2.img')

source_attr = {'file': target_vol.path()}
source = ElementTree.SubElement(disk, 'source', source_attr)

# Target dict contains the target device and the type of bus available
target_attr = {'dev': 'sdd', 'bus': 'scsi'}
target = ElementTree.SubElement(disk, 'target', target_attr)

disk_xml = ElementTree.tostring(disk, 'unicode')

print(disk_xml)
domain = client.lookupByName("vm-ubuntu-focal-lxd-1")
domain.detachDevice(disk_xml)