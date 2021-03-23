import libvirt
from nocloud.exception import FuckYouLibvirtError
# Parameters
LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
DOMAIN_NAME = 'vm-ubuntu-focal-lxd-1'

client = libvirt.open(LIBVIRT_URI)

try:
    domain = client.lookupByName(DOMAIN_NAME)
    domain.create()
except libvirt.libvirtError:
    a = FuckYouLibvirtError()
    print(a.getLibvirtRawErrorData())
