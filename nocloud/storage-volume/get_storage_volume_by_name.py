import libvirt

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
ERR_VOL_NOT_FOUND = 'Volume "{}" not found in "{}" pool.'
INFO_VOLUME_ACTIVATING = 'Pool "{}" is inactive, temporarily activating pool...'
INFO_VOLUME_DEACTIVATING = 'Deactivating pool "{}"...'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-3'
VOL_NAME = 'focal-server-cloudimg-amd64.img'

# Internal definitions


libvirt_conn = libvirt.open(LIBVIRT_URI)

pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
pool_active = not(pool.isActive())
if pool_active:
    print(INFO_VOLUME_ACTIVATING.format(STORAGE_POOL_NAME))
    pool.create()
try:
    disk = pool.storageVolLookupByName(VOL_NAME)
    print(disk.name())
except libvirt.libvirtError:
    print(ERR_VOL_NOT_FOUND)
if pool_active:
    print(INFO_VOLUME_DEACTIVATING.format(STORAGE_POOL_NAME))
    pool.destroy()
