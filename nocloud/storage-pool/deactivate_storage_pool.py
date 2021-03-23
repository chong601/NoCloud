import libvirt

# String definitions
WARN_POOL_ALREADY_INACTIVE = 'Pool {} is already deactivated.'
INFO_POOL_DEACTIVATED = 'Pool {} deactivated.'


# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
POOL_NAME = 'vm-ubuntu-focal-lxd-4'

# Internal definitions


libvirt_conn = libvirt.open(LIBVIRT_URI)

# Can use any available lookup methods to find a pool
pool = libvirt_conn.storagePoolLookupByName(POOL_NAME)
if pool.isActive() == libvirt.VIR_STORAGE_POOL_INACTIVE:
    print(WARN_POOL_ALREADY_INACTIVE.format(POOL_NAME))
elif pool.isActive() != libvirt.VIR_STORAGE_POOL_INACTIVE:
    pool.destroy()
    print(INFO_POOL_DEACTIVATED.format(POOL_NAME))
else:
    print("FIXME PLS")
