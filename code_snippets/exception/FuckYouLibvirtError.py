import libvirt


class FuckYouLibvirtError(Exception):

    VIR_ERR_NUMBER_DICT = {
        # enum virErrorNumber {
        #
        # VIR_ERR_OK 	= 	0 (0x0)
        libvirt.VIR_ERR_OK: 'No errors',
        # internal error
        # VIR_ERR_INTERNAL_ERROR 	= 	1 (0x1)
        libvirt.VIR_ERR_INTERNAL_ERROR: 'An internal error has occured',
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
        libvirt.VIR_ERR_XEN_CALL: 'Error occured when attempting a Xen hypervisor call',
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
        libvirt.VIR_ERR_RPC: 'An RPC error occured',
        # error from a GNUTLS call
        # VIR_ERR_GNUTLS_ERROR 	= 	40 (0x28)
        libvirt.VIR_ERR_GNUTLS_ERROR: 'A GNU TLS error occured',
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
        libvirt.VIR_ERR_OPERATION_INVALID: 'The operation is not applicable right now'
        # failed to start interface driver
        # VIR_WAR_NO_INTERFACE 	= 	56 (0x38)
        # interface driver not running
        # VIR_ERR_NO_INTERFACE 	= 	57 (0x39)
        # invalid interface object
        # VIR_ERR_INVALID_INTERFACE 	= 	58 (0x3a)
        # more than one matching interface found
        # VIR_ERR_MULTIPLE_INTERFACES 	= 	59 (0x3b)
        # failed to start nwfilter driver
        # VIR_WAR_NO_NWFILTER 	= 	60 (0x3c)
        # invalid nwfilter object
        # VIR_ERR_INVALID_NWFILTER 	= 	61 (0x3d)
        # nw filter pool not found
        # VIR_ERR_NO_NWFILTER 	= 	62 (0x3e)
        # nw filter pool not found
        # VIR_ERR_BUILD_FIREWALL 	= 	63 (0x3f)
        # failed to start secret storage
        # VIR_WAR_NO_SECRET 	= 	64 (0x40)
        # invalid secret
        # VIR_ERR_INVALID_SECRET 	= 	65 (0x41)
        # secret not found
        # VIR_ERR_NO_SECRET 	= 	66 (0x42)
        # unsupported configuration construct
        # VIR_ERR_CONFIG_UNSUPPORTED 	= 	67 (0x43)
        # timeout occurred during operation
        # VIR_ERR_OPERATION_TIMEOUT 	= 	68 (0x44)
        # a migration worked, but making the VM persist on the dest host failed
        # VIR_ERR_MIGRATE_PERSIST_FAILED 	= 	69 (0x45)
        # a synchronous hook script failed
        # VIR_ERR_HOOK_SCRIPT_FAILED 	= 	70 (0x46)
        # invalid domain snapshot
        # VIR_ERR_INVALID_DOMAIN_SNAPSHOT 	= 	71 (0x47)
        # domain snapshot not found
        # VIR_ERR_NO_DOMAIN_SNAPSHOT 	= 	72 (0x48)
        # stream pointer not valid
        # VIR_ERR_INVALID_STREAM 	= 	73 (0x49)
        # valid API use but unsupported by the given driver
        # VIR_ERR_ARGUMENT_UNSUPPORTED 	= 	74 (0x4a)
        # storage pool probe failed
        # VIR_ERR_STORAGE_PROBE_FAILED 	= 	75 (0x4b)
        # storage pool already built
        # VIR_ERR_STORAGE_POOL_BUILT 	= 	76 (0x4c)
        # force was not requested for a risky domain snapshot revert
        # VIR_ERR_SNAPSHOT_REVERT_RISKY 	= 	77 (0x4d)
        # operation on a domain was canceled/aborted by user
        # VIR_ERR_OPERATION_ABORTED 	= 	78 (0x4e)
        # authentication cancelled
        # VIR_ERR_AUTH_CANCELLED 	= 	79 (0x4f)
        # The metadata is not present
        # VIR_ERR_NO_DOMAIN_METADATA 	= 	80 (0x50)
        # Migration is not safe
        # VIR_ERR_MIGRATE_UNSAFE 	= 	81 (0x51)
        # integer overflow
        # VIR_ERR_OVERFLOW 	= 	82 (0x52)
        # action prevented by block copy job
        # VIR_ERR_BLOCK_COPY_ACTIVE 	= 	83 (0x53)
        # The requested operation is not supported
        # VIR_ERR_OPERATION_UNSUPPORTED 	= 	84 (0x54)
        # error in ssh transport driver
        # VIR_ERR_SSH 	= 	85 (0x55)
        # guest agent is unresponsive, not running or not usable
        # VIR_ERR_AGENT_UNRESPONSIVE 	= 	86 (0x56)
        # resource is already in use
        # VIR_ERR_RESOURCE_BUSY 	= 	87 (0x57)
        # operation on the object/resource was denied
        # VIR_ERR_ACCESS_DENIED 	= 	88 (0x58)
        # error from a dbus service
        # VIR_ERR_DBUS_SERVICE 	= 	89 (0x59)
        # the storage vol already exists
        # VIR_ERR_STORAGE_VOL_EXIST 	= 	90 (0x5a)
        # given CPU is incompatible with host CPU
        # VIR_ERR_CPU_INCOMPATIBLE 	= 	91 (0x5b)
        # XML document doesn't validate against schema
        # VIR_ERR_XML_INVALID_SCHEMA 	= 	92 (0x5c)
        # Finish API succeeded but it is expected to return NULL
        # VIR_ERR_MIGRATE_FINISH_OK 	= 	93 (0x5d)
        # authentication unavailable
        # VIR_ERR_AUTH_UNAVAILABLE 	= 	94 (0x5e)
        # Server was not found
        # VIR_ERR_NO_SERVER 	= 	95 (0x5f)
        # Client was not found
        # VIR_ERR_NO_CLIENT 	= 	96 (0x60)
        # guest agent replies with wrong id to guest-sync command (DEPRECATED)
        # VIR_ERR_AGENT_UNSYNCED 	= 	97 (0x61)
        # error in libssh transport driver
        # VIR_ERR_LIBSSH 	= 	98 (0x62)
        # fail to find the desired device
        # VIR_ERR_DEVICE_MISSING 	= 	99 (0x63)
        # invalid nwfilter binding
        # VIR_ERR_INVALID_NWFILTER_BINDING 	= 	100 (0x64)
        # no nwfilter binding
        # VIR_ERR_NO_NWFILTER_BINDING 	= 	101 (0x65)
        # invalid domain checkpoint
        # VIR_ERR_INVALID_DOMAIN_CHECKPOINT 	= 	102 (0x66)
        # domain checkpoint not found
        # VIR_ERR_NO_DOMAIN_CHECKPOINT 	= 	103 (0x67)
        # domain backup job id not found
        # VIR_ERR_NO_DOMAIN_BACKUP 	= 	104 (0x68)
        # invalid network port object
        # VIR_ERR_INVALID_NETWORK_PORT 	= 	105 (0x69)
        # the network port already exist
        # VIR_ERR_NETWORK_PORT_EXIST 	= 	106 (0x6a)
        # network port not found
        # VIR_ERR_NO_NETWORK_PORT 	= 	107 (0x6b)
        # no domain's hostname found
        # VIR_ERR_NO_HOSTNAME 	= 	108 (0x6c)
        # checkpoint can't be used
        # VIR_ERR_CHECKPOINT_INCONSISTENT 	= 	109 (0x6d)
        # more than one matching domain found
        # VIR_ERR_MULTIPLE_DOMAINS 	= 	110 (0x6e)
        # THE END OF ERROR STRUCT
        # VIR_ERR_NUMBER_LAST 	= 	111 (0x6f)
        #
        # }
    }
