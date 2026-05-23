import libvirt
from xml.etree import ElementTree
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

DISK_TYPE = 'file'
DRIVER_NAME = 'qemu'
DRIVER_SUBDRIVER = 'qcow2'
DISK_NAME = 'disk-2.img'
TARGET_DOMAIN = POOL_NAME = 'vm-ubuntu-focal-lxd-1'
TARGET_DEVICE = 'sde'
TARGET_BUS = 'scsi'

# Source attr contains the details of the source disk, in the
target_pool = client.storagePoolLookupByName(POOL_NAME)
target_vol = target_pool.storageVolLookupByName(DISK_NAME)

SOURCE_DISK = target_vol.path()


# create XML definition
disk_attr = {'type': DISK_TYPE}
disk = ElementTree.Element('disk', disk_attr)

# Note: driver attr format is as follows:
# name: the driver (usually QEMU)
# driver: the subdriver (raw, qcow2, qed, etc)
driver_attr = {'name': DRIVER_NAME, 'driver': DRIVER_SUBDRIVER}
driver = ElementTree.SubElement(disk, 'driver', driver_attr)

source_attr = {'file': SOURCE_DISK}
source = ElementTree.SubElement(disk, 'source', source_attr)

# Target dict contains the target device and the type of bus available
target_attr = {'dev': TARGET_DEVICE, 'bus': TARGET_BUS}
target = ElementTree.SubElement(disk, 'target', target_attr)

disk_xml = ElementTree.tostring(disk, 'unicode')

print(disk_xml)
domain = client.lookupByName(TARGET_DOMAIN)
domain.attachDevice(disk_xml)
