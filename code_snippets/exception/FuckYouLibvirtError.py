import libvirt


# Finally a functional and usablle libvirt exception system that doesn't suck.
class FuckYouLibvirtError(Exception):

    VIR_ERR_NUMBER_DICT = {
        # enum virErrorNumber {
        #
        # VIR_ERR_OK 	= 	0 (0x0)
        libvirt.VIR_ERR_OK: 'No errors',
        # internal error
        # VIR_ERR_INTERNAL_ERROR 	= 	1 (0x1)
        libvirt.VIR_ERR_INTERNAL_ERROR: 'An internal error has occurred',
        # memory allocation failure
        # VIR_ERR_NO_MEMORY 	    = 	2 (0x2)
        libvirt.VIR_ERR_NO_MEMORY: 'Host {} has encountered an internal error',
        # no support for this function
        # VIR_ERR_NO_SUPPORT 	    = 	3 (0x3)
        libvirt.VIR_ERR_NO_SUPPORT: 'This function is not supported',
        # could not resolve hostname
        # VIR_ERR_UNKNOWN_HOST 	    = 	4 (0x4)
        libvirt.VIR_ERR_UNKNOWN_HOST: 'Unable to resolve hostname',
        # can't connect to hypervisor
        # VIR_ERR_NO_CONNECT 	= 	5 (0x5)
        libvirt.VIR_ERR_NO_CONNECT: 'Unable to connect to hypervisor',
        # invalid connection object
        # VIR_ERR_INVALID_CONN 	= 	6 (0x6)
        libvirt.VIR_ERR_INVALID_CONN: 'The connection object is invalid',
        # invalid domain object
        # VIR_ERR_INVALID_DOMAIN 	= 	7 (0x7)
        libvirt.VIR_ERR_INVALID_DOMAIN: 'The domain object is invalid',
        # invalid function argument
        # VIR_ERR_INVALID_ARG 	= 	8 (0x8)
        libvirt.VIR_ERR_INVALID_ARG: 'Invalid function argument has been passed to this function',
        # a command to hypervisor failed
        # VIR_ERR_OPERATION_FAILED 	= 	9 (0x9)
        # FIXME: test it and put the right line
        libvirt.VIR_ERR_OPERATION_FAILED: 'A hypervisor command failed',
        # a HTTP GET command to failed
        # VIR_ERR_GET_FAILED 	= 	10 (0xa)
        libvirt.VIR_ERR_GET_FAILED: 'An HTTP GET operation failed',
        # a HTTP POST command to failed
        # VIR_ERR_POST_FAILED 	= 	11 (0xb)
        libvirt.VIR_ERR_POST_FAILED: 'An HTTP POST operation failed',
        # unexpected HTTP error code
        # VIR_ERR_HTTP_ERROR 	= 	12 (0xc)
        libvirt.VIR_ERR_HTTP_ERROR: 'libvirt received an unexpected HTTP error code',
        # failure to serialize an S-Expr
        # VIR_ERR_SEXPR_SERIAL 	= 	13 (0xd)
        libvirt.VIR_ERR_SEXPR_SERIAL: 'libvirt failed to serialize S-Expression',
        # could not open Xen hypervisor control
        # VIR_ERR_NO_XEN 	= 	14 (0xe)
        # FIXME: check if Xen control is called an interface
        libvirt.VIR_ERR_NO_XEN: 'Unable to open Xen hypervisor control interface',
        # failure doing an hypervisor call
        # VIR_ERR_XEN_CALL 	= 	15 (0xf)
        libvirt.VIR_ERR_XEN_CALL: 'Error occurred when attempting a Xen hypervisor call',
        # unknown OS type
        # VIR_ERR_OS_TYPE 	= 	16 (0x10)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_OS_TYPE: 'Unknown OS type',
        # missing kernel information
        # VIR_ERR_NO_KERNEL 	= 	17 (0x11)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_KERNEL: 'Missing required kernel information',
        # missing root device information
        # VIR_ERR_NO_ROOT 	= 	18 (0x12)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_ROOT: 'Missing required root device information',
        # missing source device information
        # VIR_ERR_NO_SOURCE 	= 	19 (0x13)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_SOURCE: 'Missing required source device information',
        # missing target device information
        # VIR_ERR_NO_TARGET 	= 	20 (0x14)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_TARGET: 'Missing required target device information',
        # missing domain name information
        # VIR_ERR_NO_NAME 	= 	21 (0x15)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_NAME: 'Missing required domain name information',
        # missing domain OS information
        # VIR_ERR_NO_OS 	= 	22 (0x16)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_OS: 'Missing required operating system information',
        # missing domain devices information
        # VIR_ERR_NO_DEVICE 	= 	23 (0x17)
        # FIXME: Check if this error message is related to missing details in domain XML
        libvirt.VIR_ERR_NO_DEVICE: 'Missing required device information',
        # could not open Xen Store control
        # VIR_ERR_NO_XENSTORE 	= 	24 (0x18)
        # FIXME: Check if Xen Store control is called in interface
        # also TODO: check if Xen Store support is required
        libvirt.VIR_ERR_NO_XENSTORE: 'Unable to open Xen Store control interface',
        # too many drivers registered
        # VIR_ERR_DRIVER_FULL 	= 	25 (0x19)
        libvirt.VIR_ERR_DRIVER_FULL: 'Unable to register driver: Too many drivers loaded',
        # not supported by the drivers (DEPRECATED)
        # VIR_ERR_CALL_FAILED 	= 	26 (0x1a)
        libvirt.VIR_ERR_CALL_FAILED: 'DEPRECATED: Function called is not supported by the driver',
        # an XML description is not well formed or broken
        # VIR_ERR_XML_ERROR 	= 	27 (0x1b)
        libvirt.VIR_ERR_XML_ERROR: 'Received XML data is not well formed',
        # the domain already exist
        # VIR_ERR_DOM_EXIST 	= 	28 (0x1c)
        libvirt.VIR_ERR_DOM_EXIST: 'Domain already exists',
        # operation forbidden on read-only connections
        # VIR_ERR_OPERATION_DENIED 	= 	29 (0x1d)
        libvirt.VIR_ERR_OPERATION_DENIED: 'An operation was attempted on a read-only libvirt connection',
        # failed to open a conf file
        # VIR_ERR_OPEN_FAILED 	= 	30 (0x1e)
        libvirt.VIR_ERR_OPEN_FAILED: 'Unable to open configuration file',
        # failed to read a conf file
        # VIR_ERR_READ_FAILED 	= 	31 (0x1f)
        libvirt.VIR_ERR_READ_FAILED: 'Unable to read configuration file',
        # failed to parse a conf file
        # VIR_ERR_PARSE_FAILED 	= 	32 (0x20)
        libvirt.VIR_ERR_PARSE_FAILED: 'Unable to parse configuration file',
        # failed to parse the syntax of a conf file
        # VIR_ERR_CONF_SYNTAX 	= 	33 (0x21)
        libvirt.VIR_ERR_CONF_SYNTAX: 'Syntax error encountered in configuration file',
        # failed to write a conf file
        # VIR_ERR_WRITE_FAILED 	= 	34 (0x22)
        libvirt.VIR_ERR_WRITE_FAILED: 'Unable to write configuration file',
        # detail of an XML error
        # VIR_ERR_XML_DETAIL 	= 	35 (0x23)
        # um what?
        # FIXME: test it and put in the right line
        libvirt.VIR_ERR_XML_DETAIL: '',
        # invalid network object
        # VIR_ERR_INVALID_NETWORK 	= 	36 (0x24)
        libvirt.VIR_ERR_INVALID_NETWORK: 'Invalid network object',
        # the network already exist
        # VIR_ERR_NETWORK_EXIST 	= 	37 (0x25)
        libvirt.VIR_ERR_NETWORK_EXIST: 'Network already exists',
        # general system call failure
        # VIR_ERR_SYSTEM_ERROR 	= 	38 (0x26)
        libvirt.VIR_ERR_SYSTEM_ERROR: 'The host encountered a system error',
        # some sort of RPC error
        # VIR_ERR_RPC 	= 	39 (0x27)
        libvirt.VIR_ERR_RPC: 'An RPC error occurred',
        # error from a GNUTLS call
        # VIR_ERR_GNUTLS_ERROR 	= 	40 (0x28)
        libvirt.VIR_ERR_GNUTLS_ERROR: 'A GNU TLS error occurred',
        # failed to start network
        # VIR_WAR_NO_NETWORK 	= 	41 (0x29)
        libvirt.VIR_WAR_NO_NETWORK: 'Warning: Unable to start network',
        # domain not found or unexpectedly disappeared
        # VIR_ERR_NO_DOMAIN 	= 	42 (0x2a)
        libvirt.VIR_ERR_NO_DOMAIN: 'Domain not found',
        # network not found
        # VIR_ERR_NO_NETWORK 	= 	43 (0x2b)
        libvirt.VIR_ERR_NO_NETWORK: 'Error: Network is not found',
        # invalid MAC address
        # VIR_ERR_INVALID_MAC 	= 	44 (0x2c)
        libvirt.VIR_ERR_INVALID_MAC: 'Supplied MAC address is invalid',
        # authentication failed
        # VIR_ERR_AUTH_FAILED 	= 	45 (0x2d)
        # TODO: figure out where this error is used
        libvirt.VIR_ERR_AUTH_FAILED: 'Authentication failure',
        # invalid storage pool object
        # VIR_ERR_INVALID_STORAGE_POOL 	= 	46 (0x2e)
        libvirt.VIR_ERR_INVALID_STORAGE_POOL: 'The storage pool object is invalid',
        # invalid storage vol object
        # VIR_ERR_INVALID_STORAGE_VOL 	= 	47 (0x2f)
        libvirt.VIR_ERR_INVALID_STORAGE_VOL: 'The storage volume object is invalid',
        # failed to start storage
        # VIR_WAR_NO_STORAGE 	= 	48 (0x30)
        libvirt.VIR_WAR_NO_STORAGE: 'Warning: Unable to start storage',
        # storage pool not found
        # VIR_ERR_NO_STORAGE_POOL 	= 	49 (0x31)
        libvirt.VIR_ERR_NO_STORAGE_POOL: 'Storage pool not found',
        # storage volume not found
        # VIR_ERR_NO_STORAGE_VOL 	= 	50 (0x32)
        libvirt.VIR_ERR_NO_STORAGE_VOL: 'Storage volume not found',
        # failed to start node driver
        # VIR_WAR_NO_NODE 	= 	51 (0x33)
        libvirt.VIR_WAR_NO_NODE: 'Warning: Failed to stat node driver',
        # invalid node device object
        # VIR_ERR_INVALID_NODE_DEVICE 	= 	52 (0x34)
        libvirt.VIR_ERR_INVALID_NODE_DEVICE: 'The node device object is invalid',
        # node device not found
        # VIR_ERR_NO_NODE_DEVICE 	= 	53 (0x35)
        libvirt.VIR_ERR_NO_NODE_DEVICE: 'Node device is not found',
        # security model not found
        # VIR_ERR_NO_SECURITY_MODEL 	= 	54 (0x36)
        libvirt.VIR_ERR_NO_SECURITY_MODEL: 'Security model not found',
        # operation is not applicable at this time
        # VIR_ERR_OPERATION_INVALID 	= 	55 (0x37)
        libvirt.VIR_ERR_OPERATION_INVALID: 'The operation is not applicable right now',
        # failed to start interface driver
        # VIR_WAR_NO_INTERFACE 	= 	56 (0x38)
        libvirt.VIR_WAR_NO_INTERFACE: 'Interface driver failed to start',
        # interface driver not running
        # VIR_ERR_NO_INTERFACE 	= 	57 (0x39)
        libvirt.VIR_ERR_NO_INTERFACE: 'Interface driver is not running',
        # invalid interface object
        # VIR_ERR_INVALID_INTERFACE 	= 	58 (0x3a)
        libvirt.VIR_ERR_INVALID_INTERFACE: 'The interface object is invalid',
        # more than one matching interface found
        # VIR_ERR_MULTIPLE_INTERFACES 	= 	59 (0x3b)
        libvirt.VIR_ERR_MULTIPLE_INTERFACES: 'Multiple interfaces are found',
        # failed to start nwfilter driver
        # VIR_WAR_NO_NWFILTER 	= 	60 (0x3c)
        libvirt.VIR_WAR_NO_NWFILTER: 'Network filter driver failed to start',
        # invalid nwfilter object
        # VIR_ERR_INVALID_NWFILTER 	= 	61 (0x3d)
        libvirt.VIR_ERR_INVALID_NWFILTER: 'The network filter object is invalid',
        # nw filter pool not found
        # VIR_ERR_NO_NWFILTER 	= 	62 (0x3e)
        libvirt.VIR_ERR_NO_NWFILTER: 'Network filter pool not found',
        # nw filter pool not found
        # VIR_ERR_BUILD_FIREWALL 	= 	63 (0x3f)
        # FIXME: is this related to unable to build firewall?
        libvirt.VIR_ERR_BUILD_FIREWALL: 'Unable to build firewall rules',
        # failed to start secret storage
        # VIR_WAR_NO_SECRET 	= 	64 (0x40)
        libvirt.VIR_WAR_NO_SECRET: 'Warning: Failed to start libvirt secret storage',
        # invalid secret
        # VIR_ERR_INVALID_SECRET 	= 	65 (0x41)
        libvirt.VIR_ERR_INVALID_SECRET: 'Invalid secret',
        # secret not found
        # VIR_ERR_NO_SECRET 	= 	66 (0x42)
        libvirt.VIR_ERR_NO_SECRET: 'Requested secret is not found',
        # unsupported configuration construct
        # VIR_ERR_CONFIG_UNSUPPORTED 	= 	67 (0x43)
        libvirt.VIR_ERR_CONFIG_UNSUPPORTED: 'Unsupported configuration',
        # timeout occurred during operation
        # VIR_ERR_OPERATION_TIMEOUT 	= 	68 (0x44)
        libvirt.VIR_ERR_OPERATION_TIMEOUT: 'Time occurred during operation',
        # a migration worked, but making the VM persist on the dest host failed
        # VIR_ERR_MIGRATE_PERSIST_FAILED 	= 	69 (0x45)
        libvirt.VIR_ERR_MIGRATE_PERSIST_FAILED: 'Unable to persist migrated domain',
        # a synchronous hook script failed
        # VIR_ERR_HOOK_SCRIPT_FAILED 	= 	70 (0x46)
        libvirt.VIR_ERR_HOOK_SCRIPT_FAILED: 'A synchronous hook script failed',
        # invalid domain snapshot
        # VIR_ERR_INVALID_DOMAIN_SNAPSHOT 	= 	71 (0x47)
        # FIXME: put a valid message
        libvirt.VIR_ERR_INVALID_DOMAIN_SNAPSHOT: 'Invalid domain snapshot',
        # domain snapshot not found
        # VIR_ERR_NO_DOMAIN_SNAPSHOT 	= 	72 (0x48)
        libvirt.VIR_ERR_NO_DOMAIN_SNAPSHOT: 'Domain snapshot not found',
        # stream pointer not valid
        # VIR_ERR_INVALID_STREAM 	= 	73 (0x49)
        # FIXME: define a better message
        libvirt.VIR_ERR_INVALID_STREAM: 'Stream pointer is not valid',
        # valid API use but unsupported by the given driver
        # VIR_ERR_ARGUMENT_UNSUPPORTED 	= 	74 (0x4a)
        libvirt.VIR_ERR_ARGUMENT_UNSUPPORTED: 'This API is not supported by the driver',
        # storage pool probe failed
        # VIR_ERR_STORAGE_PROBE_FAILED 	= 	75 (0x4b)
        libvirt.VIR_ERR_STORAGE_PROBE_FAILED: 'Failed to probe storage pool',
        # storage pool already built
        # VIR_ERR_STORAGE_POOL_BUILT 	= 	76 (0x4c)
        libvirt.VIR_ERR_STORAGE_POOL_BUILT: 'The storage pool already exists',
        # force was not requested for a risky domain snapshot revert
        # VIR_ERR_SNAPSHOT_REVERT_RISKY 	= 	77 (0x4d)
        libvirt.VIR_ERR_SNAPSHOT_REVERT_RISKY: 'A mandatory force command is required for this snapshot restore',
        # operation on a domain was canceled/aborted by user
        # VIR_ERR_OPERATION_ABORTED 	= 	78 (0x4e)
        libvirt.VIR_ERR_OPERATION_ABORTED: 'Domain operation was cancelled or aborted by user',
        # authentication cancelled
        # VIR_ERR_AUTH_CANCELLED 	= 	79 (0x4f)
        libvirt.VIR_ERR_AUTH_CANCELLED: 'An authentication operation was cancelled',
        # The metadata is not present
        # VIR_ERR_NO_DOMAIN_METADATA 	= 	80 (0x50)
        libvirt.VIR_ERR_NO_DOMAIN_METADATA: 'Domain metadata is not found',
        # Migration is not safe
        # VIR_ERR_MIGRATE_UNSAFE 	= 	81 (0x51)
        libvirt.VIR_ERR_MIGRATE_UNSAFE: 'Domain migration is not safe for current state',
        # integer overflow
        # VIR_ERR_OVERFLOW 	= 	82 (0x52)
        libvirt.VIR_ERR_OVERFLOW: 'Integer overflow is detected',
        # action prevented by block copy job
        # VIR_ERR_BLOCK_COPY_ACTIVE 	= 	83 (0x53)
        libvirt.VIR_ERR_BLOCK_COPY_ACTIVE: 'Requested operation was not performed due to an active block copy operation',
        # The requested operation is not supported
        # VIR_ERR_OPERATION_UNSUPPORTED 	= 	84 (0x54)
        libvirt.VIR_ERR_OPERATION_UNSUPPORTED: 'Requested operation was unsupported',
        # error in ssh transport driver
        # VIR_ERR_SSH 	= 	85 (0x55)
        libvirt.VIR_ERR_SSH: 'An error was encountered on SSH transport driver',
        # guest agent is unresponsive, not running or not usable
        # VIR_ERR_AGENT_UNRESPONSIVE 	= 	86 (0x56)
        libvirt.VIR_ERR_AGENT_UNRESPONSIVE: 'Guest agent on this domain is unresponsive, not running, installed or usable',
        # resource is already in use
        # VIR_ERR_RESOURCE_BUSY 	= 	87 (0x57)
        libvirt.VIR_ERR_RESOURCE_BUSY: 'Requested resource is currently in use',
        # operation on the object/resource was denied
        # VIR_ERR_ACCESS_DENIED 	= 	88 (0x58)
        libvirt.VIR_ERR_ACCESS_DENIED: 'Access denied when accessing an object or resource',
        # error from a dbus service
        # VIR_ERR_DBUS_SERVICE 	= 	89 (0x59)
        libvirt.VIR_ERR_DBUS_SERVICE: 'An error occured from the D-Bus service',
        # the storage vol already exists
        # VIR_ERR_STORAGE_VOL_EXIST 	= 	90 (0x5a)
        libvirt.VIR_ERR_STORAGE_VOL_EXIST: 'Storage volume already exists',
        # given CPU is incompatible with host CPU
        # VIR_ERR_CPU_INCOMPATIBLE 	= 	91 (0x5b)
        libvirt.VIR_ERR_CPU_INCOMPATIBLE: 'The provided CPU configuration is not compatible with the host CPU configuration',
        # XML document doesn't validate against schema
        # VIR_ERR_XML_INVALID_SCHEMA 	= 	92 (0x5c)
        libvirt.VIR_ERR_XML_INVALID_SCHEMA: 'XML validation failed due to invalid schema',
        # Finish API succeeded but it is expected to return NULL
        # VIR_ERR_MIGRATE_FINISH_OK 	= 	93 (0x5d)
        # Bruh what
        libvirt.VIR_ERR_MIGRATE_FINISH_OK: 'Migration completed, but received unexpected data (expected NULL)',
        # authentication unavailable
        # VIR_ERR_AUTH_UNAVAILABLE 	= 	94 (0x5e)
        libvirt.VIR_ERR_AUTH_UNAVAILABLE: 'Authentication is currently unavailable',
        # Server was not found
        # VIR_ERR_NO_SERVER 	= 	95 (0x5f)
        libvirt.VIR_ERR_NO_SERVER: 'Server was not found',
        # Client was not found
        # VIR_ERR_NO_CLIENT 	= 	96 (0x60)
        libvirt.VIR_ERR_NO_CLIENT: 'Client was not found',
        # guest agent replies with wrong id to guest-sync command (DEPRECATED)
        # VIR_ERR_AGENT_UNSYNCED 	= 	97 (0x61)
        libvirt.VIR_ERR_AGENT_UNSYNCED: 'DEPRECATED: Guest agent replied with a wrong ID for a guest-sync command',
        # error in libssh transport driver
        # VIR_ERR_LIBSSH 	= 	98 (0x62)
        libvirt.VIR_ERR_LIBSSH: 'An error occurred on libSSH transport driver',
        # fail to find the desired device
        # VIR_ERR_DEVICE_MISSING 	= 	99 (0x63)
        libvirt.VIR_ERR_DEVICE_MISSING: 'Device is not found',
        # invalid nwfilter binding
        # VIR_ERR_INVALID_NWFILTER_BINDING 	= 	100 (0x64)
        libvirt.VIR_ERR_INVALID_NWFILTER_BINDING: 'Invalid network filter binding',
        # no nwfilter binding
        # VIR_ERR_NO_NWFILTER_BINDING 	= 	101 (0x65)
        libvirt.VIR_ERR_NO_NWFILTER_BINDING: 'Network filter binding not found',
        # invalid domain checkpoint
        # VIR_ERR_INVALID_DOMAIN_CHECKPOINT 	= 	102 (0x66)
        libvirt.VIR_ERR_INVALID_DOMAIN_CHECKPOINT: 'Invalid domain checkpoint',
        # domain checkpoint not found
        # VIR_ERR_NO_DOMAIN_CHECKPOINT 	= 	103 (0x67)
        libvirt.VIR_ERR_NO_DOMAIN_CHECKPOINT: 'Requested domain checkpoint not found',
        # domain backup job id not found
        # VIR_ERR_NO_DOMAIN_BACKUP 	= 	104 (0x68)
        libvirt.VIR_ERR_NO_DOMAIN_BACKUP: 'Domain backup not found',
        # invalid network port object
        # VIR_ERR_INVALID_NETWORK_PORT 	= 	105 (0x69)
        libvirt.VIR_ERR_INVALID_NETWORK_PORT: 'Invalid network port',
        # the network port already exist
        # VIR_ERR_NETWORK_PORT_EXIST 	= 	106 (0x6a)
        libvirt.VIR_ERR_NETWORK_PORT_EXIST: 'The network port already exists',
        # network port not found
        # VIR_ERR_NO_NETWORK_PORT 	= 	107 (0x6b)
        libvirt.VIR_ERR_NO_NETWORK_PORT: 'Network port not found',
        # no domain's hostname found
        # VIR_ERR_NO_HOSTNAME 	= 	108 (0x6c)
        # UHHHHHH WHY IS IT NOT FOUND

        # checkpoint can't be used
        # VIR_ERR_CHECKPOINT_INCONSISTENT 	= 	109 (0x6d)
        # THIS IS MISSING TOO

        # more than one matching domain found
        # VIR_ERR_MULTIPLE_DOMAINS 	= 	110 (0x6e)

        # THE END OF ERROR STRUCT
        # VIR_ERR_NUMBER_LAST 	= 	111 (0x6f)
        #
        # }
    }

    VIR_ERR_DOMAIN_DICT = {
        # enum virErrorDomain {
        # VIR_FROM_NONE 	= 	0 (0x0)
        # Error at Xen hypervisor layer
        # VIR_FROM_XEN 	= 	1 (0x1)
        libvirt.VIR_FROM_XEN: 'Error from Xen hypervisor',
        # Error at connection with xend daemon
        # VIR_FROM_XEND 	= 	2 (0x2)
        libvirt.VIR_FROM_XEND: 'Error from Xend daemon',
        # Error at connection with xen store
        # VIR_FROM_XENSTORE 	= 	3 (0x3)
        libvirt.VIR_FROM_XENSTORE: 'Error from Xen Store',
        # Error in the S-Expression code
        # VIR_FROM_SEXPR 	= 	4 (0x4)
        libvirt.VIR_FROM_SEXPR: 'Error from S-Expression',
        # Error in the XML code
        # VIR_FROM_XML 	= 	5 (0x5)
        libvirt.VIR_FROM_XML: 'Error from XML code',
        # Error when operating on a domain
        # VIR_FROM_DOM 	= 	6 (0x6)
        libvirt.VIR_FROM_DOM: 'Error from domain management',
        # Error in the XML-RPC code
        # VIR_FROM_RPC 	= 	7 (0x7)
        libvirt.VIR_FROM_RPC: 'Error from XML-RPC',
        # Error in the proxy code; unused since 0.8.6
        # VIR_FROM_PROXY 	= 	8 (0x8)
        libvirt.VIR_FROM_PROXY: 'Error from proxy',
        # Error in the configuration file handling
        # VIR_FROM_CONF 	= 	9 (0x9)
        libvirt.VIR_FROM_CONF: 'Error from configuration file handling',
        # Error at the QEMU daemon
        # VIR_FROM_QEMU 	= 	10 (0xa)
        libvirt.VIR_FROM_QEMU: 'Error from QEMU daemon',
        # Error when operating on a network
        # VIR_FROM_NET 	= 	11 (0xb)
        # FIXME: Check the use of this and rephrase the error message
        libvirt.VIR_FROM_NET: 'Error from managing network',
        # Error from test driver
        # VIR_FROM_TEST 	= 	12 (0xc)
        libvirt.VIR_FROM_TEST: 'Error from test driver',
        # Error from remote driver
        # VIR_FROM_REMOTE 	= 	13 (0xd)
        libvirt.VIR_FROM_REMOTE: 'Error from remote driver',
        # Error from OpenVZ driver
        # VIR_FROM_OPENVZ 	= 	14 (0xe)
        libvirt.VIR_FROM_OPENVZ: 'Error from OpenVZ driver',
        # Error at Xen XM layer
        # VIR_FROM_XENXM 	= 	15 (0xf)
        libvirt.VIR_FROM_XENXM: 'Error from Xen XM layer',
        # Error in the Linux Stats code
        # VIR_FROM_STATS_LINUX 	= 	16 (0x10)
        # FIXME: Rephrase this message as soon as the source is found
        libvirt.VIR_FROM_STATS_LINUX: 'Error from Stats Linux',
        # Error from Linux Container driver
        # VIR_FROM_LXC 	= 	17 (0x11)
        libvirt.VIR_FROM_LXC: 'Error from Linux Containers (LXC) driver',
        # Error from storage driver
        # VIR_FROM_STORAGE 	= 	18 (0x12)
        libvirt.VIR_FROM_STORAGE: 'Error from storage driver',
        # Error from network config
        # VIR_FROM_NETWORK 	= 	19 (0x13)
        libvirt.VIR_FROM_NETWORK: 'Error from network configuration',
        # Error from domain config
        # VIR_FROM_DOMAIN 	= 	20 (0x14)
        libvirt.VIR_FROM_DOMAIN: 'Error from domain configuration',
        # Error at the UML driver; unused since 5.0.0
        # VIR_FROM_UML 	= 	21 (0x15)
        libvirt.VIR_FROM_UML: 'Error from UML driver',
        # Error from node device monitor
        # VIR_FROM_NODEDEV 	= 	22 (0x16)
        libvirt.VIR_FROM_NODEDEV: 'Error from node device monitor',
        # Error from xen inotify layer
        # VIR_FROM_XEN_INOTIFY 	= 	23 (0x17)
        libvirt.VIR_FROM_XEN_INOTIFY: 'Error from Xen inotify layer',
        # Error from security framework
        # VIR_FROM_SECURITY 	= 	24 (0x18)
        libvirt.VIR_FROM_SECURITY: 'Error from security',
        # Error from VirtualBox driver
        # VIR_FROM_VBOX 	= 	25 (0x19)
        libvirt.VIR_FROM_VBOX: 'Error from VirtualBox driver',
        # Error when operating on an interface
        # VIR_FROM_INTERFACE 	= 	26 (0x1a)
        # FIXME: Rewrite the message when the use of this domain is known
        libvirt.VIR_FROM_INTERFACE: 'Error during modifying interface',
        # The OpenNebula driver no longer exists. Retained for ABI/API compat only
        # VIR_FROM_ONE 	= 	27 (0x1b)
        # BYEBYE OpenNebula support
        libvirt.VIR_FROM_ONE: 'Error from OpenNebula One driver',
        # Error from ESX driver
        # VIR_FROM_ESX 	= 	28 (0x1c)
        libvirt.VIR_FROM_ESX: 'Error from ESX driver',
        # Error from the phyp driver, unused since 6.0.0
        # VIR_FROM_PHYP 	= 	29 (0x1d)
        # I have NO IDEA that IBM made their own hypervisor. TIL.
        libvirt.VIR_FROM_PHYP: 'Error from IBM POWER Hypervisor driver',
        # Error from secret storage
        # VIR_FROM_SECRET 	= 	30 (0x1e)
        libvirt.VIR_FROM_SECRET: 'Error from secret storage subsystem',
        # Error from CPU driver
        # VIR_FROM_CPU 	= 	31 (0x1f)
        libvirt.VIR_FROM_CPU: 'Error from CPU driver',
        # Error from XenAPI
        # VIR_FROM_XENAPI 	= 	32 (0x20)
        libvirt.VIR_FROM_XENAPI: 'Error from Xen API (XAPI) driver',
        # Error from network filter driver
        # VIR_FROM_NWFILTER 	= 	33 (0x21)
        libvirt.VIR_FROM_NWFILTER: 'Error from network filter driver',
        # Error from Synchronous hooks
        # VIR_FROM_HOOK 	= 	34 (0x22)
        libvirt.VIR_FROM_HOOK: 'Error from synchronous hooks',
        # Error from domain snapshot
        # VIR_FROM_DOMAIN_SNAPSHOT 	= 	35 (0x23)
        libvirt.VIR_FROM_DOMAIN_SNAPSHOT: 'Error from domain snapshot',
        # Error from auditing subsystem
        # VIR_FROM_AUDIT 	= 	36 (0x24)
        libvirt.VIR_FROM_AUDIT: 'Error from audit subsystem',
        # Error from sysinfo/SMBIOS
        # VIR_FROM_SYSINFO 	= 	37 (0x25)
        libvirt.VIR_FROM_SYSINFO: 'Error from sysinfo/SMBIOS',
        # Error from I/O streams
        # VIR_FROM_STREAMS 	= 	38 (0x26)
        libvirt.VIR_FROM_STREAMS: 'Error from streams',
        # Error from VMware driver
        # VIR_FROM_VMWARE 	= 	39 (0x27)
        libvirt.VIR_FROM_VMWARE: 'Error from VMware driver',
        # Error from event loop impl
        # VIR_FROM_EVENT 	= 	40 (0x28)
        # Error from libxenlight driver
        # VIR_FROM_LIBXL 	= 	41 (0x29)
        # Error from lock manager
        # VIR_FROM_LOCKING 	= 	42 (0x2a)
        # Error from Hyper-V driver
        # VIR_FROM_HYPERV 	= 	43 (0x2b)
        # Error from capabilities
        # VIR_FROM_CAPABILITIES 	= 	44 (0x2c)
        # Error from URI handling
        # VIR_FROM_URI 	= 	45 (0x2d)
        # Error from auth handling
        # VIR_FROM_AUTH 	= 	46 (0x2e)
        # Error from DBus
        # VIR_FROM_DBUS 	= 	47 (0x2f)
        # Error from Parallels
        # VIR_FROM_PARALLELS 	= 	48 (0x30)
        # Error from Device
        # VIR_FROM_DEVICE 	= 	49 (0x31)
        # Error from libssh2 connection transport
        # VIR_FROM_SSH 	= 	50 (0x32)
        # Error from lockspace
        # VIR_FROM_LOCKSPACE 	= 	51 (0x33)
        # Error from initctl device communication
        # VIR_FROM_INITCTL 	= 	52 (0x34)
        # Error from identity code
        # VIR_FROM_IDENTITY 	= 	53 (0x35)
        # Error from cgroups
        # VIR_FROM_CGROUP 	= 	54 (0x36)
        # Error from access control manager
        # VIR_FROM_ACCESS 	= 	55 (0x37)
        # Error from systemd code
        # VIR_FROM_SYSTEMD 	= 	56 (0x38)
        # Error from bhyve driver
        # VIR_FROM_BHYVE 	= 	57 (0x39)
        # Error from crypto code
        # VIR_FROM_CRYPTO 	= 	58 (0x3a)
        # Error from firewall
        # VIR_FROM_FIREWALL 	= 	59 (0x3b)
        # Error from polkit code
        # VIR_FROM_POLKIT 	= 	60 (0x3c)
        # Error from thread utils
        # VIR_FROM_THREAD 	= 	61 (0x3d)
        # Error from admin backend
        # VIR_FROM_ADMIN 	= 	62 (0x3e)
        # Error from log manager
        # VIR_FROM_LOGGING 	= 	63 (0x3f)
        # Error from Xen xl config code
        # VIR_FROM_XENXL 	= 	64 (0x40)
        # Error from perf
        # VIR_FROM_PERF 	= 	65 (0x41)
        # Error from libssh connection transport
        # VIR_FROM_LIBSSH 	= 	66 (0x42)
        # Error from resource control
        # VIR_FROM_RESCTRL 	= 	67 (0x43)
        # Error from firewalld
        # VIR_FROM_FIREWALLD 	= 	68 (0x44)
        # Error from domain checkpoint
        # VIR_FROM_DOMAIN_CHECKPOINT 	= 	69 (0x45)
        # Error from TPM
        # VIR_FROM_TPM 	= 	70 (0x46)
        # Error from BPF code
        # VIR_FROM_BPF 	= 	71 (0x47)
        #
        # VIR_ERR_DOMAIN_LAST 	= 	72 (0x48)
        #
        # }
    }

    VIR_ERR_LEVEL_DICT = {
        # enum virErrorLevel {
        # VIR_ERR_NONE 	= 	0 (0x0)
        libvirt.VIR_ERR_NONE: 'None',
        # A simple warning
        # VIR_ERR_WARNING 	= 	1 (0x1)
        libvirt.VIR_ERR_WARNING: 'Warning',
        # An error
        # VIR_ERR_ERROR 	= 	2 (0x2)
        libvirt.VIR_ERR_ERROR: 'Error'
        # }
    }

    def __init__(self):
        self._errorDetails = libvirt.virGetLastError()
        self.code, self.domain, self.message, self.level, self.str1, self.str2, self.str3, self.int1, self.int2 = self._errorDetails

    def getRawErrorDataFromLibvirt(self):
        return self._errorDetails

    def getErrorNumberMessage(self):
        return self.VIR_ERR_NUMBER_DICT.get(self.code)

    def getErrorDomainMessage(self):
        return self.VIR_ERR_DOMAIN_DICT.get(self.domain)

    def getErrorLevelMessage(self):
        return self.VIR_ERR_LEVEL_DICT.get(self.level)