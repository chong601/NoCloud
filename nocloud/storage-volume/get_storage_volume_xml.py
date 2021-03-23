import libvirt

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
ERR_POOL_NOT_FOUND = 'Pool "{}" is not found.'
ERR_VOLUME_NOT_FOUND = 'Volume "{}" is not found in pool "{}".'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-1'
DISK_NAME = 'focal-server-cloudimg-amd64.img'

# Internal definitions
pool = disk = None
libvirt_conn = libvirt.open(LIBVIRT_URI)
try:
    pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
except libvirt.libvirtError:
    print(ERR_POOL_NOT_FOUND.format(STORAGE_POOL_NAME))
    exit(1)
if pool.isActive() == libvirt.VIR_STORAGE_POOL_INACTIVE:
    pool.create()
try:
    disk = pool.storageVolLookupByName(DISK_NAME)
except libvirt.libvirtError:
    print(ERR_VOLUME_NOT_FOUND.format(DISK_NAME, STORAGE_POOL_NAME))
    exit(1)
print(disk.XMLDesc())
