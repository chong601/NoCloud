import libvirt

# String definitions
ERR_VOL_EXISTS = "Error: A volume has been found in {} pool. Please remove the volume before " \
                 "proceeding."
ERR_MULTIPLE_VOL_EXISTS = "Error: Multiple volumes has been found in {} pool. Please remove the " \
                          "volumes before proceeding."
INFO_POOL_DELETED = "Pool deleted successfully"

# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
POOL_TYPE = 'dir'
POOL_NAME = 'vm-ubuntu-focal-lxd-4'


# Internal definitions

libvirt_conn = libvirt.open(LIBVIRT_URI)
pool_to_delete = libvirt_conn.storagePoolLookupByName(POOL_NAME)

# this logic sucks balls that I have no choice because my hands are goddamn tied
if pool_to_delete.isActive() == libvirt.VIR_STORAGE_POOL_INACTIVE:
    pool_to_delete.create()
    if pool_to_delete.numOfVolumes() == 1:
        print(ERR_VOL_EXISTS.format(POOL_NAME))
        exit(1)
    elif pool_to_delete.numOfVolumes() > 1:
        print(ERR_MULTIPLE_VOL_EXISTS.format(POOL_NAME))
        exit(1)
    pool_to_delete.destroy()

# The Pinnacle of libvirt horrible design: calling undefine() will blindly drop the pool
# without checking if the pool has no volumes.
# Good news is that undefining a pool doesn't delete the volumes, but it makes it inaccessible
# by libvirt till the pool is back.
#
# Fun fact: your domains will remain working if you drop the pool because apparently libvirt
# handles storage by its own and they gives zero fucks about pools/volumes if the VM is created
# with an absolute path to the disk, YET it creates a pool for you if you created a VM using
# virt-install.
#
# Fuck libvirt.
pool_to_delete.undefine()
