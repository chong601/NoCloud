import libvirt
client = libvirt.open("qemu+ssh://chong601@10.102.0.5/system")

for f in range(1, 4):

    domain = client.lookupByName("vm-ubuntu-focal-lxd-{}".format(f))

    fullSize, allocatedSize, physicalSize = domain.blockInfo("/zfs-storage-test/kvm-area/{}/disk-1.img".format(domain.name()))
    print("{} disk usage: {} total, {} allocated, {} physical".format(domain.name(), fullSize/1024/1024/1024, allocatedSize/1024/1024/1024, physicalSize/1024/1024/1024))
