import libvirt

# String definitions
WARN_POOL_ALREADY_AUTOSTARTED = 'Pool {} is already autostarted.'
INFO_POOL_AUTOSTARTED = 'Pool {} set to autostart.'


# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
POOL_NAME = 'vm-ubuntu-focal-lxd-3'

# Internal definitions
AUTOSTARTED = STORAGE_POOL_IS_AUTOSTARTED = 1
NOT_AUTOSTARTED = 0

libvirt_conn = libvirt.open(LIBVIRT_URI)

# Can use any available lookup methods to find a pool
pool = libvirt_conn.storagePoolLookupByName(POOL_NAME)
print(pool.autostart())
if pool.autostart() == AUTOSTARTED:
    print(WARN_POOL_ALREADY_AUTOSTARTED.format(POOL_NAME))
elif pool.autostart() != NOT_AUTOSTARTED:
    pool.setAutostart(AUTOSTARTED)
    print(INFO_POOL_AUTOSTARTED.format(POOL_NAME))
else:
    print("FIXME PLS")
