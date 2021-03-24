import libvirt

# Constants
GIGABYTES = 1024*1024*1024
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
ERR_POOL_NOT_FOUND = 'Pool "{}" is not found.'
ERR_VOLUME_NOT_FOUND = 'Volume "{}" is not found in pool "{}".'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-1'
DISK_NAME = 'focal-server-cloudimg-amd64.img'
ADDITIONAL_DISK_SPACE = 3*GIGABYTES

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

# From libvirt volume resize documentation:
#
# > Normally, the operation treats @capacity as the new size in bytes;
# > but if @flags contains VIR_STORAGE_VOL_RESIZE_DELTA,
# > then @capacity represents the size difference to add to the current size.
# > It is up to the storage pool implementation whether unaligned requests
# > are rounded up to the next valid boundary, or rejected.
#
# OK libvirt, you do you I guess.
disk.resize(ADDITIONAL_DISK_SPACE, libvirt.VIR_STORAGE_VOL_RESIZE_DELTA)
