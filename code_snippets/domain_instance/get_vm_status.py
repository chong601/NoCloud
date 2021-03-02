import libvirt

LIBVIRT_URI = 'qemu+ssh://chong601@10.102.0.5/system'
DOMAIN_NAME = 'vm-ubuntu-focal-lxd-1'

client = libvirt.open(LIBVIRT_URI)

try:
    domain = client.lookupByName(DOMAIN_NAME)
    state, reason = domain.state()
    # VIR_DOMAIN_NOSTATE = 0(0x0)
    # VIR_DOMAIN_RUNNING = 1(0x1)
    # VIR_DOMAIN_BLOCKED = 2(0x2)
    # VIR_DOMAIN_PAUSED = 3(0x3)
    # VIR_DOMAIN_SHUTDOWN = 4(0x4)
    # VIR_DOMAIN_SHUTOFF = 5(0x5)
    # VIR_DOMAIN_CRASHED = 6(0x6)
    # VIR_DOMAIN_PMSUSPENDED = 7(0x7)
    # VIR_DOMAIN_LAST = 8(0x8)
    # libvirt is so simple. That it really wanna make everything as complicated as they want.
    # Sure, I can see why they love granularity, but uuuuuuuuuugh this is painful to make
    if state == libvirt.VIR_DOMAIN_NOSTATE:
        print('Domain {} is currently in unknown state'.format(DOMAIN_NAME))
        # enum
        # virDomainNostateReason
        # {
        #
        #     VIR_DOMAIN_NOSTATE_UNKNOWN = 0(0x0)
        #     VIR_DOMAIN_NOSTATE_LAST = 1(0x1)
        #
        # }
        # WELL FUCKING DONE LOL
        if reason == libvirt.VIR_DOMAIN_NOSTATE_UNKNOWN:
            print('Reason: Unknown')
    elif state == libvirt.VIR_DOMAIN_RUNNING:
        print('Instance "{}" is currently running'.format(DOMAIN_NAME))
        # enum virDomainRunningReason {
        #
        # VIR_DOMAIN_RUNNING_UNKNOWN 	= 	0 (0x0)
        # VIR_DOMAIN_RUNNING_BOOTED 	= 	1 (0x1) 	#normal startup from boot
        # VIR_DOMAIN_RUNNING_MIGRATED 	= 	2 (0x2) 	#migrated from another host
        # VIR_DOMAIN_RUNNING_RESTORED 	= 	3 (0x3) 	#restored from a state file
        # VIR_DOMAIN_RUNNING_FROM_SNAPSHOT 	= 	4 (0x4) 	#restored from snapshot
        # VIR_DOMAIN_RUNNING_UNPAUSED 	= 	5 (0x5) 	#returned from paused state
        # VIR_DOMAIN_RUNNING_MIGRATION_CANCELED 	= 	6 (0x6) 	#returned from migration
        # VIR_DOMAIN_RUNNING_SAVE_CANCELED 	= 	7 (0x7) 	#returned from failed save process
        # VIR_DOMAIN_RUNNING_WAKEUP 	= 	8 (0x8) 	#returned from pmsuspended due to wakeup event
        # VIR_DOMAIN_RUNNING_CRASHED 	= 	9 (0x9) 	#resumed from crashed
        # VIR_DOMAIN_RUNNING_POSTCOPY 	= 	10 (0xa) 	#running in post-copy migration mode
        # VIR_DOMAIN_RUNNING_LAST 	= 	11 (0xb)
        #
        # }
        if reason == libvirt.VIR_DOMAIN_RUNNING_UNKNOWN:
            # HOW CAN YOU DON'T KNOW YOUR OWN RUNNING STATE?
            print('Reason: Unknown')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_BOOTED:
            print('Reason: The instance is booted up normally')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_MIGRATED:
            print('Reason: The instance has been migrated successfully')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_RESTORED:
            print('Reason: The instance has been restored from state file')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_FROM_SNAPSHOT:
            print('Reason: The instance has been restored from a snapshot')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_UNPAUSED:
            print('Reason: The instance has returned from paused state')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_MIGRATION_CANCELED:
            print('Reason: The instance has returned from a cancelled migration')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_SAVE_CANCELED:
            print('Reason: The instance has returned from a failed save process')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_WAKEUP:
            print('Reason: The instance has resumed from sleep event')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_CRASHED:
            print('Reason: The instance has resumed from a crashed state')
        elif reason == libvirt.VIR_DOMAIN_RUNNING_POSTCOPY:
            print('Reason: The instance is currently in post-copy migration mode')
        else:
            print('New state has been defined by upstream libvirt. Please raise a bug with us')

    elif state == libvirt.VIR_DOMAIN_BLOCKED:
        print('Instance "{}" is currently blocked'.format(DOMAIN_NAME))
        # enum
        # virDomainBlockedReason
        # {
        #
        #       VIR_DOMAIN_BLOCKED_UNKNOWN = 0(0x0) #the reason is unknown
        #       VIR_DOMAIN_BLOCKED_LAST = 1(0x1)
        #
        # }
        # What ze fauk is blocked is for then if the reason is fucking unknown???
        # At least the reason is just unknown, but man....
        if reason == libvirt.VIR_DOMAIN_RUNNING_UNKNOWN:
            # HOW CAN YOU DON'T KNOW YOUR OWN RUNNING STATE?
            print('Reason: Unknown')
        else:
            print('New state has been defined by upstream libvirt. Please raise a bug with us.')

    elif state == libvirt.VIR_DOMAIN_PAUSED:
        print('Instance "{}" is currently paused'.format(DOMAIN_NAME))
        #
        #
        # enum virDomainPausedReason {
        #
        # VIR_DOMAIN_PAUSED_UNKNOWN 	        = 	0 (0x0) 	# the reason is unknown
        # VIR_DOMAIN_PAUSED_USER 	            = 	1 (0x1) 	# paused on user request
        # VIR_DOMAIN_PAUSED_MIGRATION 	        = 	2 (0x2) 	# paused for offline migration
        # VIR_DOMAIN_PAUSED_SAVE 	            = 	3 (0x3) 	# paused for save
        # VIR_DOMAIN_PAUSED_DUMP 	            = 	4 (0x4) 	# paused for offline core dump
        # VIR_DOMAIN_PAUSED_IOERROR 	        = 	5 (0x5) 	# paused due to a disk I/O error
        # VIR_DOMAIN_PAUSED_WATCHDOG 	        = 	6 (0x6) 	# paused due to a watchdog event
        # VIR_DOMAIN_PAUSED_FROM_SNAPSHOT 	    = 	7 (0x7) 	# paused after restoring from snapshot
        # VIR_DOMAIN_PAUSED_SHUTTING_DOWN 	    = 	8 (0x8) 	# paused during shutdown process
        # VIR_DOMAIN_PAUSED_SNAPSHOT 	        = 	9 (0x9) 	# paused while creating a snapshot
        # VIR_DOMAIN_PAUSED_CRASHED 	        = 	10 (0xa) 	# paused due to a guest crash
        # VIR_DOMAIN_PAUSED_STARTING_UP 	    = 	11 (0xb) 	# the domain is being started
        # VIR_DOMAIN_PAUSED_POSTCOPY 	        = 	12 (0xc) 	# paused for post-copy migration
        # VIR_DOMAIN_PAUSED_POSTCOPY_FAILED 	= 	13 (0xd) 	# paused after failed post-copy
        # VIR_DOMAIN_PAUSED_LAST 	            = 	14 (0xe)    # this is useless
        #
        # }
        msg = {
            libvirt.VIR_DOMAIN_PAUSED_UNKNOWN: "Unknown",
            libvirt.VIR_DOMAIN_PAUSED_USER: "The instance is paused by user request",
            libvirt.VIR_DOMAIN_PAUSED_MIGRATION: "The instance is paused for offline migration",
            libvirt.VIR_DOMAIN_PAUSED_SAVE: "The instance is paused for save operation",
            libvirt.VIR_DOMAIN_PAUSED_DUMP: "The instance is paused for offline core dump",
            libvirt.VIR_DOMAIN_PAUSED_IOERROR: "The instance is paused due to I/O error",
            libvirt.VIR_DOMAIN_PAUSED_WATCHDOG: "The instance is paused due to watchdog event",
            libvirt.VIR_DOMAIN_PAUSED_FROM_SNAPSHOT: "The instance is paused after from a snapshot restore",
            libvirt.VIR_DOMAIN_PAUSED_SHUTTING_DOWN: "The instance is paused during shut down process", # NOTE: libvirt DOES NOT KNOW if the host is shutting down, until the host signals it's about to go down
            libvirt.VIR_DOMAIN_PAUSED_SNAPSHOT: "The instance is paused while creating a snapshot",
            libvirt.VIR_DOMAIN_PAUSED_CRASHED: "The instance is paused because the guest instance crashed",
            libvirt.VIR_DOMAIN_PAUSED_STARTING_UP: "The instance is starting up from paused state",
            libvirt.VIR_DOMAIN_PAUSED_POSTCOPY: "The instance is paused for post-copy operation",
            libvirt.VIR_DOMAIN_PAUSED_POSTCOPY_FAILED: "The instance is paused after a faied post-copy operation"
        }.get(reason)
        if not msg:
            print("New state has been defined by upstream libvirt. Please raise a bug with us")
        else:
            print(f"Reason: {msg}")
    # Shut down state != Shut off state
    # Shut down state means it's currently shutting down
    # Also, due to how libvirt works. you don't know if the domain has started shutting down until **the guest informs
    # libvirt it's going down**
    elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
        print('Instance "{}" is currently shutting down.'.format(DOMAIN_NAME))

        # enum virDomainShutdownReason
        # {
        #
        #     VIR_DOMAIN_SHUTDOWN_UNKNOWN   = 0(0x0)    # the reason is unknown
        #     VIR_DOMAIN_SHUTDOWN_USER      = 1(0x1)    # shutting down on user request
        #     VIR_DOMAIN_SHUTDOWN_LAST      = 2(0x2)
        #
        # }
        if reason == libvirt.VIR_DOMAIN_SHUTDOWN_UNKNOWN:
            # Just... why.
            print('Reason: Unknown')
        elif reason == libvirt.VIR_DOMAIN_SHUTDOWN_USER:
            print('Reason: The instance is shutting down by user request')
    # VIR_DOMAIN_SHUTOFF = 5(0x5)
    # VIR_DOMAIN_CRASHED = 6(0x6)
    # VIR_DOMAIN_PMSUSPENDED = 7(0x7)
    # VIR_DOMAIN_LAST = 8(0x8)
    elif state == libvirt.VIR_DOMAIN_SHUTOFF:
        print('Domain "{}" is currently shut down'.format(DOMAIN_NAME))
        # enum virDomainShutoffReason {
        # VIR_DOMAIN_SHUTOFF_UNKNOWN 		= 	0 (0x0) 	# the reason is unknown
        # VIR_DOMAIN_SHUTOFF_SHUTDOWN 		= 	1 (0x1) 	# normal shutdown
        # VIR_DOMAIN_SHUTOFF_DESTROYED 		= 	2 (0x2) 	# forced poweroff
        # VIR_DOMAIN_SHUTOFF_CRASHED 		= 	3 (0x3) 	# domain crashed
        # VIR_DOMAIN_SHUTOFF_MIGRATED 		= 	4 (0x4) 	# migrated to another host
        # VIR_DOMAIN_SHUTOFF_SAVED 		    = 	5 (0x5) 	# saved to a file
        # VIR_DOMAIN_SHUTOFF_FAILED 		= 	6 (0x6) 	# domain failed to start
        # VIR_DOMAIN_SHUTOFF_FROM_SNAPSHOT 	= 	7 (0x7) 	# restored from a snapshot which was taken while domain was shutoff
        # VIR_DOMAIN_SHUTOFF_DAEMON 		= 	8 (0x8) 	# daemon decides to kill domain during reconnection processing
        # VIR_DOMAIN_SHUTOFF_LAST 		    = 	9 (0x9)     # this is useless
        #
        # }
        msg = {
            libvirt.VIR_DOMAIN_SHUTOFF_UNKNOWN: "Unknown"
            libvirt.VIR_DOMAIN_SHUTOFF_SHUTDOWN: "The domain was shut down normally"
            libvirt.VIR_DOMAIN_SHUTOFF_DESTROYED: "The domain was shut down using force shut down method"
            libvirt.VIR_DOMAIN_SHUTOFF_CRASHED: "The domain was shut down due to a crash"
            libvirt.VIR_DOMAIN_SHUTOFF_MIGRATED: "The domain was shut down normally"
            libvirt.VIR_DOMAIN_SHUTOFF_SAVED: "The domain was shut down normally"
            libvirt.VIR_DOMAIN_SHUTOFF_FAILED: "The domain was shut down normally"
            libvirt.VIR_DOMAIN_SHUTOFF_FROM_SNAPSHOT: "The domain was shut down normally"
            libvirt.VIR_DOMAIN_SHUTOFF_DAEMON: "The domain was shut down normally"
        }.get(reason)
        if not msg:
            print("New state has been defined by upstream libvirt. Please raise a bug with us")
        else:
            print(f"Reason: {msg}")



except libvirt.libvirtError:
    # TODO: check for errors
    print('Internal error')
