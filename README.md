Qubes Dead Man's Switch
====
This repo provides three packages:
- qubes-app-dms
- qubes-app-dms-timeout
- qubes-app-dms-bluetooth

qubes-app-dms
----
This package, to be installed in Dom0, provides the RPC service to respond to a triggered dead man's switch.

qubes-app-dms-timeout
----
This package, to be installed in Dom0, implements a timeout-based dead man's switch: if the lock screen is enabled for a certain duration (default 2h, configurable in `/rw/usrlocal/etc/qubes-dms/timeout.conf`), the dead man's switch is triggered.

qubes-app-dms-bluetooth
----
This package, to be installed in an AppVM or NetVM, implements a Bluetooth device proximity-based dead man's switch: after a particular Bluetooth device is seen, any loss of contact triggers the dead man's switch.  This requires configuration post-install: edit the installed `/rw/usrlocal/etc/qubes-dms/bluetooth.conf` file and add the Bluetooth MAC address of your desired device.
