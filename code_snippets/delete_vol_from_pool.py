import libvirt
from xml.etree import ElementTree

# String definitions
ERR_INSTANCE_NOT_SHUTOFF = """Error: Instance \"{}\" is still running."""\
           """Shut down or power off the instance before deleting the volume"""
ERR_DISK_NOT_DETACHED = """Error: Disk is currently attached to instance \"{}\"."""\
           """Detach the disk first before deleting the volume"""
INFO_VOLUME_DELETED = "Volume deleted successfully."

# Parameters
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")
DOMAIN_NAME = POOL_NAME = 'vm-ubuntu-focal-lxd-1'
DISK_NAME = 'disk-2.img'
domain = client.lookupByName(DOMAIN_NAME)

# Internal definitions
XML_DISK_PATH = './devices/disk'

# find_disk.py start
xml = ElementTree.fromstring(domain.XMLDesc())
disks = xml.findall(XML_DISK_PATH)
disk_source_path = []
for disk in disks:
    if 'file' in disk.find("source").attrib:
        source = disk.find("source").attrib['file']
        disk_source_path.append(source)
    else:
        source = 'n/a'

# find_disk.py end

pool = client.storagePoolLookupByName(POOL_NAME)
volume_libvirt = pool.storageVolLookupByName(DISK_NAME)
print(volume_libvirt.path())
if domain.state() != libvirt.VIR_DOMAIN_SHUTOFF:
    print(ERR_INSTANCE_NOT_SHUTOFF.format(DOMAIN_NAME))
elif volume_libvirt.path() in disk_source_path:
    print(ERR_DISK_NOT_DETACHED.format(DOMAIN_NAME))
else:
    volume_libvirt.delete()
    print(INFO_VOLUME_DELETED)
