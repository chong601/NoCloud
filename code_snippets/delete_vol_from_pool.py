import libvirt
from xml.etree import ElementTree

client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")
instance_to_delete = 'vm-ubuntu-focal-lxd-1'
domain = client.lookupByName(instance_to_delete)

# find_disk.py start
xml = ElementTree.fromstring(domain.XMLDesc())
disks = xml.findall("./devices/disk")
disk_source_path = []
for disk in disks:
    if 'file' in disk.find("source").attrib:
        source = disk.find("source").attrib['file']
        disk_source_path.append(source)
    else:
        source = 'n/a'

# find_disk.py end

pool = client.storagePoolLookupByName('vm-ubuntu-focal-lxd-1')
volume_libvirt = pool.storageVolLookupByName('disk-2.img')
print(volume_libvirt.path())
if domain.state() != libvirt.VIR_DOMAIN_SHUTOFF:
    print("Error: Instance \"{}\" is still running."
          " Shut down or power off the instance before deleting the volume".format(instance_to_delete))
elif volume_libvirt.path() in disk_source_path:
    print("Error: Disk is currently attached to instance \"{}\"."
          " Detach the disk first before deleting the volume".format(instance_to_delete))
else:
    volume_libvirt.delete()
    print("Volume deleted successfully.")
