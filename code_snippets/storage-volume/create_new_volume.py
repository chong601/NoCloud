import libvirt
from xml.etree import ElementTree
import subprocess

# Constants
MEGABYTES = 1024**2
GIGABYTES = 1024**3

# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"
DISK_NAME = 'test.img'
DISK_TYPE = 'qcow2'
DISK_SIZE = 100*GIGABYTES
HOST_FILESYSTEM = 'zfs'
ZFS_IS_DATASET = True
STORAGE_POOL_NAME = 'vm-ubuntu-focal-lxd-3'
METADATA_PREALLOCATION = 1
XML_POOL_PATH = './target'


# TODO: look into key
# ALSO TODO: make this work with paramiko
def call_qemu_img(destination, target_disk_format, disk_capacity, allocation_method):

    qemu_img_cmd = ['qemu-img', 'create', '-f', target_disk_format]
    if allocation_method == METADATA_PREALLOCATION:
        qemu_img_cmd.extend(['-o', 'preallocation={}'.format('metadata')])
    qemu_img_cmd.extend([destination, disk_capacity])
    ret = subprocess.run(qemu_img_cmd)
    return ret.returncode


client = libvirt.open(LIBVIRT_URI)
pool = client.storagePoolLookupByName(STORAGE_POOL_NAME)
volume = ElementTree.Element('volume')
name = ElementTree.SubElement(volume, 'name').text = DISK_NAME
capacity = ElementTree.SubElement(volume, 'capacity').text = str(DISK_SIZE)
target = ElementTree.SubElement(volume, 'target')
# format_attr has type which is the type of disk to create eg: raw, bochs, qcow, qcow2, qed, vmdk
format_attr = {'type': DISK_TYPE}
disk_format = ElementTree.SubElement(target, 'format', format_attr)
volume_xml = ElementTree.tostring(volume, 'unicode')
print(volume_xml)

# WARNING: ZFS DO NOT support falloc method of disk allocation
# TODO: add more disk type for other filesystems
if DISK_TYPE == 'qcow2':
    if HOST_FILESYSTEM == 'zfs' and ZFS_IS_DATASET:
        # TODO: ZFS-specific metadata preallocation
        # ZFS filesystem has one quirk that most in-tree Linux kernel doesn't have:
        #            ZFS doesn't understand falloc() write syscall.
        #
        # Which makes it a bit in a shit situation cause ZFS devs decided that rather than use other alternative syscall
        # (which understandbly they didn't do that because breaking APIs ain't a good idea),
        # they decided to do the equivalent of full-allocation. With zeroing.
        # How fun.
        #
        # Fun fact: libvirt does has it's own ZFS implementation... using ZVOLs.
        #
        # Upside: they are natively supported on RH/CentOS
        # Downside: ZVOLs are relatively less performant than datasets.
        # And in the classic RH development style, doesn't implement dataset support whatsoever.
        #
        # FUCK YOU LIBVIRT.
        # Fuck you, fuck you, fuck you, fuck you, fuck you and fuck you libvirt.
        xml = ElementTree.fromstring(pool.XMLDesc())
        disks = xml.findall(XML_POOL_PATH)
        disk_real_path = disks[0].find('path').text + '/'

        destination_path = disk_real_path + DISK_NAME

        return_code = call_qemu_img(destination_path, DISK_TYPE, DISK_SIZE, METADATA_PREALLOCATION)

        # VERY UNTESTED. DO NOT BLINDLY RUN THIS.
        volume_libvirt = pool.createXML(volume_xml, libvirt.VOL_CREATE)
    else:
        if METADATA_PREALLOCATION == libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA:
            volume_libvirt = pool.createXML(volume_xml, libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA)
        else:
            volume_libvirt = pool.createXML(volume_xml)
else:
    print("Storage type is not implemented (yet)")
