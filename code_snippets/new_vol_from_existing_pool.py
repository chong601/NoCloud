import libvirt
from xml.etree import ElementTree

# Constants
MEGABYTES = 1024**2
GIGABYTES = 1024**3

# Parameters
DISK_NAME = 'disk-2.img'
DISK_TYPE = 'qcow2'
HOST_FILESYSTEM = 'zfs'
POOL_NAME = 'vm-ubuntu-focal-lxd-1'

volume = ElementTree.Element('volume')
name = ElementTree.SubElement(volume, 'name').text = DISK_NAME
capacity = ElementTree.SubElement(volume, 'capacity').text = str(1*GIGABYTES)
target = ElementTree.SubElement(volume, 'target')
# format_attr has type which is the type of disk to create eg: raw, bochs, qcow, qcow2, qed, vmdk
format_attr = {'type': DISK_TYPE}
disk_format = ElementTree.SubElement(target, 'format', format_attr)


# TODO: look into key
def call_qemu_img(self, source, dest, target_disk_format, disk_capacity, allocation_method):
    pass


volume_xml = ElementTree.tostring(volume, 'unicode')
print(volume_xml)
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")
pool = client.storagePoolLookupByName(POOL_NAME)

# WARNING: ZFS DO NOT support falloc method of disk allocation
# TODO: add more disk type for other filesystems
if DISK_TYPE == 'qcow2':
    if HOST_FILESYSTEM == 'zfs':
        # TODO: ZFS-specific metadata preallocation
        # FUCK YOU LIBVIRT
        # call_qemu_img(source,dest,target_disk_format,disk_capacity,'metadata')
        pass
    else:
        volume_libvirt = pool.createXML(volume_xml, libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA)
else:
    print("Storage type is not implemented (yet)")



