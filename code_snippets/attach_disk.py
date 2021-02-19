import libvirt
from xml.etree import ElementTree
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# create XML definition
disk_attr = {'type': 'file'}
disk = ElementTree.Element('disk', disk_attr)

# Note: driver attr format is as follows:
# name: the driver (usually QEMU)
# driver: the subdriver (raw, qcow2, qed, etc)
driver_attr = {'name': 'qemu', 'driver': 'qcow2'}
driver = ElementTree.SubElement(disk, 'driver', driver_attr)

# Source attr contains the details of the source disk, in the
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
domain.attachDevice(disk_xml)




