# Create VM is a multi-step process:
# - create a disk OR copy a pre-configured VM OR create a disk pool and create a volume
#   - can also use filesystem-specific cloning features like ZFS or LVM snapshots
# - resize the disk to appropriate sizes
# - create Cloud-Init definitions eg: user, filesystem, packages, update
#   - optionally create custom networks rather than DHCP
# - deploy Cloud-Init configs either using `cloud-localds` or deploy to a webserver
# - create VM definitions on libvirt using libvirt Python API (oh lord pls no)
# - define into libvirt to be registered
# - start the VM

# It would be nice if we can boot to network, reboot and return to normal boot sequence but eh
from jinja2 import FileSystemLoader, Environment, select_autoescape
import subprocess, libvirt
from xml.etree import ElementTree
from uuid import UUID

# String definitions
ERR_POOL_NOT_FOUND = 'Pool "{}" is not found.'
ERR_VOLUME_NOT_FOUND = 'Volume "{}" is not found in pool "{}".'
ERR_DOMAIN_NOT_FOUND = 'Domain "{}" is not found.'

# Parameters
MEGABYTES = 1024**2
GIGABYTES = 1024**3

DOMAIN_NAME = 'vm-ubuntu-focal-cloud-init-test-4'
CLOUD_DS = 'ds=nocloud-net;s=http://{}:{}/{}/'
DISK_NAME = 'disk-2.img'
DISK_TYPE = 'qcow2'
DISK_CAPACITY = 100*GIGABYTES
HOST_FILESYSTEM = 'zfs'
POOL_NAME = 'vm-ubuntu-focal-lxd-1'

# Internal definitions
ENABLED_ESCAPES = ['html', 'xml']
DS_HOST = '10.102.7.97'
DS_PORT = '5000'
j2_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(ENABLED_ESCAPES)
)

client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

# Clone the VM pool
subprocess.run([])

# Create a new pool
# TODO: write pool storage code

# Define a new volume for libvirt to monitor
volume = ElementTree.Element('volume')
name = ElementTree.SubElement(volume, 'name').text = DISK_NAME
capacity = ElementTree.SubElement(volume, 'capacity').text = str(DISK_CAPACITY)
target = ElementTree.SubElement(volume, 'target')
# format_attr has type which is the type of disk to create eg: raw, bochs, qcow, qcow2, qed, vmdk
format_attr = {'type': DISK_TYPE}
disk_format = ElementTree.SubElement(target, 'format', format_attr)


# TODO: look into key
def call_qemu_img(self, source, dest, target_disk_format, disk_capacity, allocation_method):
    subprocess.run([])


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
# Expand the disk to appropriate size
# TODO: write vol-resize code
pool = disk = None

try:
    pool = client.storagePoolLookupByName(POOL_NAME)
except libvirt.libvirtError:
    print(ERR_POOL_NOT_FOUND.format(POOL_NAME))
    exit(1)
if pool.isActive() == libvirt.VIR_STORAGE_POOL_INACTIVE:
    pool.create()
try:
    disk = pool.storageVolLookupByName(DISK_NAME)
except libvirt.libvirtError:
    print(ERR_VOLUME_NOT_FOUND.format(DISK_NAME, POOL_NAME))
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
# This is the right place to use absolute size resizing.
# TODO: do proper size checks before blindly resizing them
disk.resize(DISK_CAPACITY, libvirt.VIR_STORAGE_VOL_RESIZE_DELTA)

# Generate domain XML
# TODO: complete Jinja2 XML implementation
# LAZINESS SUCK. Even if I have Jinja2 imports included LOL.`

# Define in libvirt
# TODO: write define domain code
domain = client.defineXML()


# Get UUID
# TODO: write getUUID() code
try:
    domain_obj = client.lookupByName(DOMAIN_NAME)
except libvirt.libvirtError:
    print(ERR_DOMAIN_NOT_FOUND.format(DOMAIN_NAME))
    exit(1)
domain_uuid = domain_obj.UUID()
# The UUID is returned in the form of actual bytes...
# What the fuck.
domain_uuid = domain_obj.UUID()

# Set SMBIOS data
# FIXME: can be combined into "Generate domain XML" section
# Absolute cancer.
# Why I need to do it this way.
final_smbios_data = CLOUD_DS.format(DS_HOST, DS_PORT, UUID(bytes=domain_uuid))

# Generate user-data
# TODO: Create sample helper code to expose user-data
# ALSO TODO: Move to ruamel.yaml if don't want to use `#cloud-config` line hack
# Cue the world's possibly drunkest and most hacky way to generate YAML.

#cloud-config
# name: chong601
# password: chong601
# chpasswd: {expire: False}
# ssh_pwauth: True
# hostname: vm - ubuntu - focal - lxd - cluster - 3
# timezone: "Asia/Kuala_Lumpur"
# package_update: true
# package_upgrade: true
# package_reboot_if_required: true
# packages:
# - qemu - guest - agent
# - haveged
# power_state:
# delay: now
# mode: reboot
# message: "Cloud-config for vm-ubuntu-focal-lxd-cluster-3 is completed. Restarting..."
# timeout: 15
# condition: True
# system_info:
#   default_user:




# Generate meta-data
# TODO: Create sample helper code to expose user-data

# Generate network data
# TODO: Figure out how to present networking data on nocloud-net Cloud-Init

# Store in DB
# TODO: long long time layer

# Start domain
# TODO: write domain lifecycle code
