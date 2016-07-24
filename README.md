Qubes Dead Man's Switch
====
The Qubes dead man's switch system consists of three components:
- qubes-app-dms
- qubes-app-dms-timeout
- qubes-app-dms-bluetooth

qubes-app-dms
----
This package, to be installed in Dom0, provides the RPC service to respond to a triggered dead man's switch.

qubes-app-dms-timeout
----
This package, to be installed in Dom0, implements a timeout-based dead man's switch: if the lock screen is enabled for a certain duration, the dead man's switch is triggered.  Once installed, it must be manually enabled:
- If desired, a different timeout period should be set in `/usr/local/etc/qubes-dms/timeout.conf`
- Enable the service: `[user@dom0 ~]$ systemctl --user enable qubes-app-dms-timeout` 

qubes-app-dms-bluetooth
----
This package, to be installed in the TemplateVM of the AppVM/NetVM/USBVM you wish to use, implements a Bluetooth device proximity-based dead man's switch: after a particular Bluetooth device is seen, any loss of contact triggers the dead man's switch.

Once installed in the appropriate TemplateVM, the specific VM which will run the monitor should be configured:
- Ensure the Bluetooth transceiver is assigned to the VM
- Insert the appropriate Bluetooth device MAC and (optionally) change parameters in `/usr/local/etc/qubes-dms/bluetooth.conf`
- Enable the service: `[user@sys-usb]$ systemctl --user enable qubes-app-dms-bluetooth`
