import libvirt
from uuid import UUID
# String definitions
ERR_DOMAIN_NOT_FOUND = 'Domain "{}" is not found.'
OUTPUT_DOMAIN_NAME = '"uuid": "{}", "domain": "{}"'

# Parameters
LIBVIRT_URI = "qemu+ssh://chong601@10.102.0.5/system"

DOMAIN_NAME = ['vm-ubuntu-focal-lxd-1',
               'vm-ubuntu-focal-lxd-2',
               'vm-ubuntu-focal-lxd-3',
               ]

client = libvirt.open(LIBVIRT_URI)

for domain_name in DOMAIN_NAME:
    try:
        domain_obj = client.lookupByName(domain_name)
    except libvirt.libvirtError:
        print(ERR_DOMAIN_NOT_FOUND.format(domain_name))
        exit(1)
    # The UUID is returned in the form of actual bytes...
    # What the fuck.
    domain_uuid = domain_obj.UUID()

    # Use UUID module to read the UUID value returned by libvirt by explicitly
    # inform the module to read it as bytes and then output in string form
    print(OUTPUT_DOMAIN_NAME.format(UUID(bytes=domain_uuid), domain_name))

for domain_name in DOMAIN_NAME:
    try:
        domain_obj = client.lookupByName(domain_name)
    except libvirt.libvirtError:
        print(ERR_DOMAIN_NOT_FOUND.format(domain_name))
        exit(1)
    # This is the sensible way to get UUID (most of the time)
    domain_uuid = domain_obj.UUIDString()

    # ... and it doesn't work the first time. Of course.
    # Because Python only accepts the following:
    #
    # UUID('{12345678-1234-5678-1234-567812345678}')
    # UUID('12345678123456781234567812345678')
    # UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
    # UUID(bytes=b'\x12\x34\x56\x78'*4)
    # UUID(bytes_le=b'\x78\x56\x34\x12\x34\x12\x78\x56' +
    #               b'\x12\x34\x56\x78\x12\x34\x56\x78')
    # UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
    # UUID(int=0x12345678123456781234567812345678)s
    #
    # ... but not the official UUID of 12345678-1234-5678-1234-567812345678
    # What the fuck Python.
    print(OUTPUT_DOMAIN_NAME.format(UUID("urn:uuid:"+domain_uuid), domain_name))
