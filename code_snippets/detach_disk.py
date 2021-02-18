import libvirt
from xml.etree import ElementTree

client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# WARNING: This will break the device on the instance if the device is still in use
# ie. mounted as a filesystem. Probably offer this feature if the instance is shut down
# Parameters
domain_name = pool_name = 'vm-ubuntu-focal-lxd-1'
disk_name = 'disk-2.img'
target_device_name = 'sdd'
target_device_bus_type = 'scsi'

# Look for domain name
domain = client.lookupByName(domain_name)
if domain.state() != libvirt.VIR_DOMAIN_SHUTOFF:
    print('Error: Instance "{}" is still running. Shut down or power off the instance before detaching the disk')
    exit(1)

# create XML definition
disk_attr = {'type': 'file'}
disk = ElementTree.Element('disk')

# Look for pool name (usually matches the domain name)
target_pool = client.storagePoolLookupByName(pool_name)

# Look for vol name
# Also libvirt volumes has "key" element in their XML, but they don't offer key lookups, wtf?
# Probably will replace this when getting volume by key code is ready
# and hopefully libvirt XML volume format doesn't change
target_vol = target_pool.storageVolLookupByName(disk_name)

# TODO: MAYBE can just get the disk definition straight from XML and use that rather than creating one from scratch?
source_attr = {'file': target_vol.path()}
source = ElementTree.SubElement(disk, 'source', source_attr)

# Target dict contains the target device and the type of bus available
target_attr = {'dev': target_device_name, 'bus': target_device_bus_type}
target = ElementTree.SubElement(disk, 'target', target_attr)

disk_xml = ElementTree.tostring(disk, 'unicode')
print(disk_xml)

domain.detachDevice(disk_xml)
