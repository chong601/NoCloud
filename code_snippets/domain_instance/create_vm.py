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

# Parameters
DOMAIN_NAME = 'vm-ubuntu-focal-cloud-init-test-4'
CLOUD_DS = 'ds=nocloud-net;s=http://{}:{}/{}/'

# Internal definitions
ENABLED_ESCAPES = ['html', 'xml']
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
# Constants
MEGABYTES = 1024**2
GIGABYTES = 1024**3

# Parameters
DISK_NAME = 'disk-2.img'
DISK_TYPE = 'qcow2'
HOST_FILESYSTEM = 'zfs'
POOL_NAME = 'vm-ubuntu-focal-lxd-1'

volume = ElementTree.Element('volume')
name = ElementTree.SubElement(volume, 'name').text = DISK_NAME
capacity = ElementTree.SubElement(volume, 'capacity').text = str(1*GIGABYTES)
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

# Generate domain XML
# TODO: complete Jinja2 XML implementation

# Define in libvirt
# TODO: write define domain code

# Get UUID
# TODO: write getUUID() code

# Set SMBIOS data
# FIXME: can be combined into "Generate domain XML" section

# Generate user-data
# TODO: Create sample helper code to expose user-data

# Generate meta-data
# TODO: Create sample helper code to expose user-data

# Generate network data
# TODO: Figure out how to present networking data on nocloud-net Cloud-Init

# Store in DB
# TODO: long long time layer

# Start domain
# TODO: write domain lifecycle code
