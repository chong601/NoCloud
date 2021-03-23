import libvirt
from xml.etree import ElementTree

client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# WARNING: This will break the device on the instance if the device is still in use
# ie. mounted as a filesystem. Probably offer this feature if the instance is shut down

# String definitions
ERR_DOMAIN_NOT_SHUTOFF = """Error: Instance "{}" is still running. 
Shut down or power off the instance before detaching the disk"""

# Parameters
DOMAIN_NAME = POOL_NAME = 'vm-ubuntu-focal-lxd-1'
DISK_NAME = 'disk-2.img'
DISK_TYPE = 'file'
TARGET_DEVICE_NAME = 'sdd'
TARGET_DEVICE_BUS_TYPE = 'scsi'


# Look for domain name
domain = client.lookupByName(DOMAIN_NAME)
if domain.state() != libvirt.VIR_DOMAIN_SHUTOFF:
    print(ERR_DOMAIN_NOT_SHUTOFF.format(DOMAIN_NAME))
    exit(1)

# create XML definition
disk_attr = {'type': DISK_TYPE}
disk = ElementTree.Element('disk')

# Look for pool name (usually matches the domain name)
target_pool = client.storagePoolLookupByName(POOL_NAME)

# Look for vol name
# Also libvirt volumes has "key" element in their XML, but they don't offer key lookups, wtf?
# Probably will replace this when getting volume by key code is ready
# and hopefully libvirt XML volume format doesn't change
target_vol = target_pool.storageVolLookupByName(DISK_NAME)

# TODO: MAYBE can just get the disk definition straight from XML and use that rather than creating one from scratch?
source_attr = {'file': target_vol.path()}
source = ElementTree.SubElement(disk, 'source', source_attr)

# Target dict contains the target device and the type of bus available
target_attr = {'dev': TARGET_DEVICE_NAME, 'bus': TARGET_DEVICE_BUS_TYPE}
target = ElementTree.SubElement(disk, 'target', target_attr)

disk_xml = ElementTree.tostring(disk, 'unicode')
print(disk_xml)

domain.detachDevice(disk_xml)
