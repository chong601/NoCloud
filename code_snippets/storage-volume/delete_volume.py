import libvirt

# Constants


# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
DISK_NAME = 'test.img'
HOST_FILESYSTEM = 'zfs'
ZFS_IS_DATASET = True
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-3'
XML_POOL_PATH = './target'
DELETE_SNAPSHOTS = True

# Internal definitions

libvirt_conn = libvirt.open(LIBVIRT_URI)
pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
disk = pool.storageVolLookupByName(DISK_NAME)

if disk is not None:
    flag = None
    if DELETE_SNAPSHOTS:
        disk.delete(libvirt.VIR_STORAGE_VOL_DELETE_WITH_SNAPSHOTS)
    else:
        disk.delete()