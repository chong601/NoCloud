import libvirt

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
INFO_VOLUME_ACTIVATING = 'Pool "{}" is inactive, temporarily activating pool...'
INFO_VOLUME_DEACTIVATING = 'Deactivating pool "{}"...'

# Parameters
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-1'

# Internal definitions


libvirt_conn = libvirt.open(LIBVIRT_URI)

pool = libvirt_conn.storagePoolLookupByName(STORAGE_POOL_NAME)
pool_active = not(pool.isActive())
if pool_active:
    print(INFO_VOLUME_ACTIVATING.format(STORAGE_POOL_NAME))
    pool.create()
# sorted() to make output look nicer
print('Available volumes:')
for volume in sorted(pool.listVolumes()):
    print("- {}".format(volume))
if pool_active:
    print(INFO_VOLUME_DEACTIVATING.format(STORAGE_POOL_NAME))
    pool.destroy()
