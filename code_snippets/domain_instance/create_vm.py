# Create VM is a multi-step process:
# TODO: update this list to reflect new functionalities that is added after the process is written
# - create a disk OR copy a pre-configured VM OR create a disk pool and create a volume
#   - can also use filesystem-specific cloning features like ZFS or LVM snapshots
# - resize the disk to appropriate sizes
# - create Cloud-Init definitions eg: user, filesystem, packages, update
#   - optionally create custom networks rather than DHCP
# - ~~deploy Cloud-Init configs either using `cloud-localds` or deploy to a webserver~~ NO NEED. WE HAVE `nocloud-net`
# - create VM definitions on libvirt using libvirt Python API (oh lord pls no)
# - define into libvirt to be registered
# - start the VM

# It would be nice if we can boot to network, reboot and return to normal boot sequence but eh
from jinja2 import FileSystemLoader, Environment, select_autoescape
import subprocess
import libvirt
from xml.etree import ElementTree
from uuid import uuid4

# String definitions
ERR_POOL_NOT_FOUND = 'Pool "{}" is not found.'
ERR_VOLUME_NOT_FOUND = 'Volume "{}" is not found in pool "{}".'
ERR_DOMAIN_NOT_FOUND = 'Domain "{}" is not found.'

# Parameters
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
MEGABYTES = 1024**2
GIGABYTES = 1024**3

DOMAIN_NAME = 'vm-ubuntu-focal-cloud-init-test-4'
CLOUD_DS = 'ds=nocloud-net;s=http://{}:{}/{}/'
DISK_NAME = 'disk-2.img'
DISK_TYPE = 'qcow2'
DISK_CAPACITY = 100*GIGABYTES

HOST_FILESYSTEM = 'zfs'
POOL_NAME = 'vm-ubuntu-focal-cloud-init-test-4'
POOL_TYPE = 'dir'
TARGET_PATH = '/zfs-storage-test/kvm-area/{}'.format(DOMAIN_NAME)
POOL_AUTOSTART = 1
ZFS_IS_DATASET = True

EMULATION_TYPE = 'kvm'
MEMORY_CAPACITY = 4
MAX_MEMORY_CAPACITY = 16
PROVISIONED_CPU_COUNT = 4
HOST_CPU_COUNT = 24
VM_UUID = str(uuid4())
SOCKET_COUNT = 1
CORE_COUNT = 24
THREAD_COUNT = 1

# Internal definitions
ENABLED_ESCAPES = ['html', 'xml']
DS_HOST = '10.102.7.97'
DS_PORT = '5000'
final_smbios_data = CLOUD_DS.format(DS_HOST, DS_PORT, VM_UUID)
BIOS_VENDOR = 'NoCloud-libvirt-QEMU-KVM'
VNC_PORT = -1
VNC_LISTEN_IP = '0.0.0.0'
DISK_PATH = '/zfs-storage-test/kvm-area'
IMAGE_NAME = 'focal-server-cloudimg-amd64.img'
j2_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(ENABLED_ESCAPES)
)

print('Connecting to libvirt host at {}...'.format(LIBVIRT_URI))
client = libvirt.open(LIBVIRT_URI)
print('libvirt host "{}" connected.'.format(client.getHostname()))
# Clone the VM pool
# TODO: Paramiko integration
# subprocess.run([])

# Create a new pool
# TODO: write pool storage code
# XML GENERATION TIME *shudders*
print('Generating new pool definition for pool name {}...'.format(POOL_NAME))
pool_attr = {'type': POOL_TYPE}
pool_root = ElementTree.Element('pool', pool_attr)
pool_name = ElementTree.SubElement(pool_root, 'name').text = POOL_NAME
pool_target = ElementTree.SubElement(pool_root, 'target')
pool_target_path = ElementTree.SubElement(pool_target, 'path').text = TARGET_PATH

pool_xml = ElementTree.tostring(pool_root, 'unicode')
print(pool_xml)
print('Pool definition complete.')
print('Informing {} to create pool "{}"...'.format(client.getHostname(), POOL_NAME))
client.storagePoolDefineXML(pool_xml)
print('Pool {} is create at {}.'.format(POOL_NAME, client.getHostname()))

print('Informing {} to set pool "{}" to autostart...')
pool_obj = client.storagePoolLookupByName(POOL_NAME)
pool_obj.setAutostart(POOL_AUTOSTART)
print('Pool {} at {} autostarted'.format(POOL_NAME, client.getHostname()))

# Define a new volume for libvirt to monitor
print('Generating definitions for volume {}"...'.format(DISK_NAME))
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
pool = client.storagePoolLookupByName(POOL_NAME)
print('Generation complete.')

print('Adding volume "{}" to pool "{}" at "{}"')
# WARNING: ZFS DO NOT support falloc method of disk allocation
# TODO: add more disk type for other filesystems
if DISK_TYPE == 'qcow2':
    if HOST_FILESYSTEM == 'zfs' and ZFS_IS_DATASET:
        # TODO: ZFS-specific metadata preallocation
        # FUCK YOU LIBVIRT
        # call_qemu_img(source,dest,target_disk_format,disk_capacity,'metadata')
        try:
            pool = client.storagePoolLookupByName(POOL_NAME)
        except libvirt.libvirtError:
            print(ERR_POOL_NOT_FOUND.format(POOL_NAME))
            exit(1)
        if pool.isActive() == libvirt.VIR_STORAGE_POOL_INACTIVE:
            pool.create()
        volume_libvirt = pool.createXML(volume_xml)
    else:
        volume_libvirt = pool.createXML(volume_xml)
else:
    print("Storage type is not implemented (yet)")
print('Volume "{}" is created on pool "{}" at "{}"'.format(DISK_NAME, POOL_NAME, client.getHostname()))
# Expand the disk to appropriate size
# TODO: write vol-resize code
print('Informing host "{}" to resize volume "{}" to {} bytes...'.format(client.getHostname(), DISK_NAME, DISK_CAPACITY))
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
print('Volume resize done.')

# Generate domain XML
# TODO: complete Jinja2 XML implementation
# LAZINESS SUCK. Even if I have Jinja2 imports included LOL.`

# Define in libvirt
# TODO: write define domain code
# ALSO TODO: MAKE THIS DOMAIN XML THING A CLASS OF ITSELF. I HATE HOW IT LOOKS RIGHT NOW.
# oooooooooooooooooooooooooooooooooooooooh fuck me why do I have to go through this...
# This kind of code is I guess why we have so many bad developers out there, but to be honest:
# - XML is hateful
# - XML APIs forced me to do this
# - the fact that libvirt **ENFORCES** the need to use XML which is just asinine
print('Generating domain definition for domain "{}"...'.format(DOMAIN_NAME))
domain_attr = {'type': EMULATION_TYPE}
xml_domain = ElementTree.Element('domain', domain_attr)
xml_name = ElementTree.SubElement(xml_domain, 'name').text = DOMAIN_NAME
xml_uuid = ElementTree.SubElement(xml_domain, 'uuid').text = VM_UUID
# Memory attributes are **strictly** required because it defaults to KiB
# 10/10 libvirt, assuming that people actually use KiB to define memory.
memory_attr = {'unit': 'GiB'}
xml_memory = ElementTree.SubElement(xml_domain, 'memory', memory_attr).text = str(MAX_MEMORY_CAPACITY)
current_memory_attr = {'unit': 'GiB'}
xml_current_memory = ElementTree.SubElement(xml_domain, 'currentMemory', current_memory_attr).text = str(MEMORY_CAPACITY)
vcpu_attr = {'current': str(PROVISIONED_CPU_COUNT)}
xml_vcpu = ElementTree.SubElement(xml_domain, 'vcpu', vcpu_attr).text = str(HOST_CPU_COUNT)
xml_os = ElementTree.SubElement(xml_domain, 'os')
os_smbios_attr = {'mode': 'sysinfo'}
xml_os_smbios = ElementTree.SubElement(xml_os, 'smbios', os_smbios_attr)
os_type_attr = {'arch': 'x86_64', 'machine': 'q35'}
xml_os_type = ElementTree.SubElement(xml_os, 'type', os_type_attr).text = 'hvm'
os_boot_attr = {'dev': 'hd'}
xml_os_boot = ElementTree.SubElement(xml_os, 'boot', os_boot_attr)
sysinfo_attr = {'type': 'smbios'}
xml_sysinfo = ElementTree.SubElement(xml_domain, 'sysinfo', sysinfo_attr)
xml_sysinfo_bios = ElementTree.SubElement(xml_sysinfo, 'bios')
sysinfo_bios_vendor_attr = {'name': 'vendor'}
xml_sysinfo_bios_entry = ElementTree.SubElement(xml_sysinfo_bios, 'entry', sysinfo_bios_vendor_attr).text = BIOS_VENDOR
xml_sysinfo_system = ElementTree.SubElement(xml_sysinfo, 'system')
sysinfo_system_manufacturer_attr = {'name': 'manufacturer'}
xml_sysinfo_system_manufacturer = ElementTree.SubElement(xml_sysinfo_system, 'entry', sysinfo_system_manufacturer_attr).text = 'KVM'
sysinfo_system_product_attr = {'name': 'product'}
xml_sysinfo_system_product = ElementTree.SubElement(xml_sysinfo_system, 'entry', sysinfo_system_product_attr).text = 'libvirt-virt-manager'
sysinfo_system_version_attr = {'name': 'version'}
xml_sysinfo_system_version = ElementTree.SubElement(xml_sysinfo_system, 'entry', sysinfo_system_version_attr).text = '0.1-alpha'
sysinfo_system_serial_attr = {'name': 'serial'}
xml_sysinfo_system_serial = ElementTree.SubElement(xml_sysinfo_system, 'entry', sysinfo_system_serial_attr).text = final_smbios_data
xml_sysinfo_chassis = ElementTree.SubElement(xml_sysinfo, 'chassis')
sysinfo_chassis_manufacturer_attr = {'name': 'manufacturer'}
xml_sysinfo_chassis_manufacturer = ElementTree.SubElement(xml_sysinfo_chassis, 'entry', sysinfo_chassis_manufacturer_attr).text = 'Dell'
sysinfo_chassis_product_attr = {'name': 'product'}
xml_sysinfo_chassis_product = ElementTree.SubElement(xml_sysinfo_chassis, 'entry', sysinfo_chassis_product_attr).text = 'PowerEdge R710'
sysinfo_chassis_version_attr = {'name': 'version'}
xml_sysinfo_chassis_version = ElementTree.SubElement(xml_sysinfo_chassis, 'entry', sysinfo_chassis_version_attr).text = '1.0'
sysinfo_chassis_serial_attr = {'name': 'serial'}
xml_sysinfo_chassis_serial = ElementTree.SubElement(xml_sysinfo_chassis, 'entry', sysinfo_chassis_serial_attr).text = 'H42H32S'
xml_features = ElementTree.SubElement(xml_domain, 'features')
xml_features_acpi = ElementTree.SubElement(xml_features, 'acpi')
xml_features_apic = ElementTree.SubElement(xml_features, 'apic')
cpu_attr = {'mode': 'host-model'}
xml_cpu = ElementTree.SubElement(xml_domain, 'cpu', cpu_attr)
cpu_topology_attr = {'sockets': str(SOCKET_COUNT), 'cores': str(CORE_COUNT), 'threads': str(THREAD_COUNT)}
xml_cpu_topology = ElementTree.SubElement(xml_cpu, 'topology', cpu_topology_attr)
clock_attr = {'offset': 'utc'}
xml_clock = ElementTree.SubElement(xml_domain, 'clock', clock_attr)
clock_timer_rtc_attr = {'name': 'rtc', 'tickpolicy': 'catchup'}
xml_clock_timer_rtc = ElementTree.SubElement(xml_clock, 'timer', clock_timer_rtc_attr)
clock_timer_pit_attr = {'name': 'pit', 'tickpolicy': 'delay'}
xml_clock_timer_pit = ElementTree.SubElement(xml_clock, 'timer', clock_timer_pit_attr)
clock_timer_hpet_attr = {'name': 'hpet', 'present': 'no'}
xml_clock_timer_hpet = ElementTree.SubElement(xml_clock, 'timer', clock_timer_hpet_attr)
xml_pm = ElementTree.SubElement(xml_domain, 'pm')
pm_suspend_mem_attr = {'enabled': 'no'}
xml_pm_suspend_mem = ElementTree.SubElement(xml_pm, 'suspend-to-mem', pm_suspend_mem_attr)
pm_suspend_disk_attr = {'enabled': 'no'}
xml_pm_suspend_disk = ElementTree.SubElement(xml_pm, 'suspend-to-disk', pm_suspend_disk_attr)
xml_devices = ElementTree.SubElement(xml_domain, 'devices')
# Do we need to define an emulator to use? Hopefully not.
# I am not stoked on hardcoding path to the emulator...
# Putting this in just in case if libvirt just doesn't wanna cooperate at all
# xml_devices_emulator = ElementTree.SubElement(xml_devices, 'emulator').text = EMULATOR_PATH
devices_disk_attr = {'type': 'file', 'device': 'disk'}
xml_devices_disk = ElementTree.SubElement(xml_devices, 'disk', devices_disk_attr)
devices_disk_driver_attr = {'name': 'qemu', 'type': 'qcow2', 'discard': 'unmap'}
xml_devices_disk_driver = ElementTree.SubElement(xml_devices_disk, 'driver', devices_disk_driver_attr)
devices_disk_source_attr = {'file': '{}/{}/{}'.format(DISK_PATH, DOMAIN_NAME, IMAGE_NAME)}
xml_devices_disk_source = ElementTree.SubElement(xml_devices_disk, 'source', devices_disk_source_attr)
devices_disk_target_attr = {'dev': 'sda', 'bus': 'scsi'}
xml_devices_disk_target = ElementTree.SubElement(xml_devices_disk, 'target', devices_disk_target_attr)
devices_controller_scsi_attr = {'type': 'scsi', 'model': 'virtio-scsi'}
xml_devices_controller_scsi = ElementTree.SubElement(xml_devices, 'controller', devices_controller_scsi_attr)
devices_controller_usb_attr = {'type': 'usb', 'model': 'qemu-xhci', 'ports': '15'}
xml_devices_controller_usb = ElementTree.SubElement(xml_devices, 'controller', devices_controller_usb_attr)
devices_interface_attr = {'type': 'network'}
xml_devices_interface = ElementTree.SubElement(xml_devices, 'interface', devices_interface_attr)
devices_interface_source_attr = {'network': 'default'}
xml_devices_interface_source = ElementTree.SubElement(xml_devices_interface, 'source', devices_interface_source_attr)
devices_interface_model_attr = {'type': 'virtio'}
xml_devices_interface_model = ElementTree.SubElement(xml_devices_interface, 'model', devices_interface_model_attr)
devices_console_type_attr = {'type': 'pty'}
xml_devices_console_type = ElementTree.SubElement(xml_devices, 'console', devices_console_type_attr)
devices_channel_attr = {'type': 'unix'}
xml_devices_channel = ElementTree.SubElement(xml_devices, 'channel', devices_channel_attr)
devices_channel_source_attr = {'mode': 'bind'}
xml_devices_channel_source = ElementTree.SubElement(xml_devices_channel, 'source', devices_channel_source_attr)
channel_target_attr = {'type': 'virtio', 'name': 'org.qemu.guest_agent.0'}
xml_channel_target = ElementTree.SubElement(xml_devices_channel, 'target', channel_target_attr)
devices_input_attr = {'type': 'tablet', 'bus': 'usb'}
devices_xml_input = ElementTree.SubElement(xml_devices, 'input', devices_input_attr)
devices_graphics_attr = {'type': 'vnc', 'port': str(VNC_PORT), 'listen': VNC_LISTEN_IP}
xml_devices_graphics = ElementTree.SubElement(xml_devices, 'graphics', devices_graphics_attr)
xml_devices_video = ElementTree.SubElement(xml_devices, 'video')
devices_video_model_attr = {'type': 'qxl'}
xml_devices_video_model = ElementTree.SubElement(xml_devices_video, 'model', devices_video_model_attr)
devices_memballoon_attr = {'model': 'virtio'}
devices_xml_memballoon = ElementTree.SubElement(xml_devices, 'memballoon', devices_memballoon_attr)
devices_rng_attr = {'model': 'virtio'}
xml_devices_rng = ElementTree.SubElement(xml_devices, 'rng', devices_rng_attr)
devices_rng_backend_attr = {'model': 'random'}
xml_devices_rng_backend = ElementTree.SubElement(xml_devices_rng, 'backend', devices_rng_backend_attr).text = '/dev/urandom'

xml_str = ElementTree.tostring(xml_domain, 'unicode')
print('Generation complete.')
print('Defining domain {} at {}'.format(DOMAIN_NAME, client.getHostname()))
domain = client.defineXML(xml_str)


# Get UUID
# TODO: write getUUID() code
# This is fucking broken logic. I hate it. And UUID is already defined up there so this is completely useless
try:
    domain_obj = client.lookupByName(DOMAIN_NAME)
    domain_uuid = domain_obj.UUID()
except libvirt.libvirtError:
    print(ERR_DOMAIN_NOT_FOUND.format(DOMAIN_NAME))
    exit(1)


# Set SMBIOS data
# FIXME: can be combined into "Generate domain XML" section
# Absolute cancer.
# Why I need to do it this way.
#
# Also, already done above.


# Generate user-data
# TODO: Create sample helper code to expose user-data
# ALSO TODO: Move to ruamel.yaml if don't want to use `#cloud-config` line hack
# Cue the world's possibly drunkest and most hacky way to generate YAML.

#cloud-config
# name: chong601
# password: chong601
# chpasswd: {expire: False}
# ssh_pwauth: True
# hostname: vm-ubuntu-focal-lxd-cluster-3
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
print('Starting domain {} at {}'.format(DOMAIN_NAME, client.getHostname()))
domain.create()
print('Domain {} is started at {}'.format(DOMAIN_NAME, client.getHostname()))