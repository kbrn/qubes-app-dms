#!/usr/bin/python
import ConfigParser
import subprocess
import time
import os
import bluetooth

config_file = '/usr/local/etc/qubes-dms/bluetooth.conf'

def initiate_panic_mode():
    """
    Sets a flag on the filesystem so the accompanying Dom0 monitor script
    knows when to trigger panic mode
    """
    #TODO: Implement writing a TOTP authentication string instead of "1"

    while True:
            try:
                trigger = subprocess.call(['/usr/lib/qubes/qrexec-client-vm', 
                                            'dom0', 
                                            'qubes.DeadMansSwitch', 
                                            '/bin/echo', '1'])
                break
            except Exception, e:
                #Is there a better way to gracefully fail here?  
                #We should maybe just loop retrying?
                print "Failed to send trigger signal; retrying in 5s..."
                time.sleep(5)

def turn_bt_on():
    """
    Turns on the Bluetooth controller, so the scans we do actually succeed 
    instead of failing by being 'unable to open controller device'
    """
    #FIXME: Find a better way to turn on the controller device.
    #FIXME: This assumes there's only one Bluetooth controller--if there's 
    #more than one, you will need to select the one you want first, or 
    #write something more complicated that turns them all on.
    #FIXME: Should do some error checking and state validation
    print 'turning on bt controller.'
    btctrl = subprocess.Popen(
                        '/bin/bluetoothctl',
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE)

    time.sleep(1)
    btctrl.stdin.write('power on\n')
    time.sleep(1)
    btctrl.stdin.write('scan on\n')
    time.sleep(1)
    btctrl.stdin.write('quit\n')
    time.sleep(1)
    print 'bt controller should be on.'

    #Just in case the process didn't end after we told it to quit:
    btctrl.terminate() 

def main():
    """
    The main domU-based monitor loop.  This code implements a very simple FSM.
    The essential components are ugly hacks, pybluez's discover_devices(),
    and permissive exception handling...
    """

    #Set up initial state by reading user prefs in config file.
    try:
        global config_file
        cfg = ConfigParser.SafeConfigParser()
        cfg.read(config_file)
        target_address = cfg.get('bluetooth', 'target_address')
        scan_interval = int(cfg.get('bluetooth', 'scan_interval'))
        graceful_fails = int(cfg.get('bluetooth', 'graceful_fails'))  
    except Exception, e:
        print 'error while reading the config file... exiting: %s' %str(e)
        exit(1)

    #Define local variables.
    states = frozenset(['disarmed', 'armed', 'triggered', 'panic'])
    cur_state = 'disarmed'
    next_state = None
    fail_count = 0
    counter = 0
    
    print 'entering main loop.'
    #FSM main loop:
    while True:
        print 'doing new iteration %d' %counter
        try:
            #Before scanning, turn on Bluetooth controller with bluetoothctl. 
            #We do this before every scan instead of just once because the 
            #Bluetooth controller turns off if the computer sleeps.
            turn_bt_on() 

            #Check if the target Bluetooth device is physically near:
            nearby_devices = bluetooth.discover_devices()
            is_around = False
            for device_addr in nearby_devices:
                if target_address == device_addr:
                    is_around = True
                    break

            #Begin FSM transition behavior:
            if(cur_state == 'disarmed'):
                if(is_around):
                    next_state = 'armed'
                else:
                    next_state = 'disarmed'
            elif(cur_state == 'armed'):
                if(is_around):
                    next_state = 'armed'
                else:
                    next_state = 'triggered'
            elif(cur_state == 'triggered'):
                if(is_around):
                    fail_count = 0
                    next_state = 'armed'
                else:
                    fail_count += 1
                    if(fail_count <= graceful_fails):
                        next_state = 'triggered'
                    else:
                        next_state = 'panic'

            log = open('/tmp/dmsstate', "w")
            log.write('{0}'.format(next_state))
            log.close()

            #Note that this compares next_state, not cur_state.
            #In the case of a panic, we want to wipe memory and die
            #as quickly as possible without waiting for the next scan_interval.
            if(next_state == 'panic'):
                initiate_panic_mode()
                exit(0)

            #Validate and update FSM state:
            if(next_state in states):
                cur_state = next_state
            else:
                #FIXME: Find a better way to crash? 
                print 'next_state %s was not in states...' %next_state
                exit(2)

            #Wait before recalculating transition functions:
            time.sleep(scan_interval)
            counter = counter + 1;

        #Exceptions sometimes happen e.g. when the computer goes to sleep 
        #in the middle of a loop; just ignore them. Wait before retrying, though
        except Exception, e:
            print 'encountered an exception in main:\n(%s)... retrying.' %str(e)
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
