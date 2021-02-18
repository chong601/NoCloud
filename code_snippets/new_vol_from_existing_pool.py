import libvirt
from xml.etree import ElementTree

MEGABYTES = 1024**2
GIGABYTES = 1024**3
volume = ElementTree.Element('volume')
name = ElementTree.SubElement(volume, 'name').text = 'disk-2.img'
capacity = ElementTree.SubElement(volume, 'capacity').text = str(1*GIGABYTES)
target = ElementTree.SubElement(volume, 'target')
# format_attr has type which is the type of disk to create eg: raw, bochs, qcow, qcow2, qed, vmdk
format_attr = {'type': 'qcow2'}
disk_format = ElementTree.SubElement(target, 'format', format_attr)

# TODO: look into key

volume_xml = ElementTree.tostring(volume, 'unicode')
print(volume_xml)

client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")
pool = client.storagePoolLookupByName('vm-ubuntu-focal-lxd-1')
volume_libvirt = pool.createXML(volume_xml, libvirt.VIR_STORAGE_VOL_CREATE_PREALLOC_METADATA)

