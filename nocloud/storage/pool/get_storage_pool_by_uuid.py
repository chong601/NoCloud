import libvirt
import uuid

# Constants
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
INFO_VOLUME_ACTIVATING = 'Pool "{}" is inactive, temporarily activating pool...'
INFO_VOLUME_DEACTIVATING = 'Deactivating pool "{}"...'

# Parameters
STORAGE_POOL_UUID = '32e7ed21-8b51-4b17-9e0b-4acc967ed140'
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-1'

# Internal definitions


libvirt_conn = libvirt.open(LIBVIRT_URI)

# Fun story: libvirt C library has two ways to get storage pool by UUID:
# - virStoragePoolLookupByUUID
# - virStoragePoolLookupByUUIDString
#
# ... and of course, the Python binding literally has the exact copy of them:
# - virConnect.storagePoolLookupByUUID
# - virConnect.storagePoolLookupByUUIDString
#
# What I don't get it is if you look at their reference, the function signature looks
# like this:
#       virStoragePoolPtr	virStoragePoolLookupByUUID	(virConnectPtr conn,
# 							                             const unsigned char * uuid)
#
#       virStoragePoolPtr	virStoragePoolLookupByUUIDString	(virConnectPtr conn,
# 							                                     const char * uuidstr)
#
# I don't know C language much, but why does libvirt need **two** versions of lookup
# by UUID? Why not just use just one of it: the string version.
# Pretty sure that the UUID library in C would happily give you string representation of
# UUID anyway right?
#
# Oh and it doesn't get any better because surprise, surprise: Python also has UUID... with its own type too.
#
# Which also means that you can do both on Python as well *facepalms*
#
# I wonder if the RH devs that decided to implement Python binding are doing it this way because either
# a) they just want to do a quick porting
# b) the devs in charge of this porting attempt doesn't seem to know that Python is a dynamically-typed language
#

pool = libvirt_conn.storagePoolLookupByUUIDString(STORAGE_POOL_UUID)
print(pool.name())
libvirt_conn.storagepoolloo
anotherpool = libvirt_conn.storagePoolLookupByUUID(uuid.UUID(STORAGE_POOL_UUID).bytes)
print(anotherpool.name())
