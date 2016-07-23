#!/bin/bash

curstate="UNBLANK"
oldtime=$(date '+%s')
timeout=$(cat /rw/usrlocal/etc/qubes-dms/timeout.conf)

while true
do
    xscreensaver-command -watch
    sleep 1
done | /usr/libexec/qubes/heartbeat | while read line
do
    if [ "$(echo $line | egrep '^(LOCK|UNBLANK)')" != "" ]
    then
        curstate=$(echo "$line" | awk '{print $1}')
        if [ "$curstate" != "UNBLANK" ]
        then
            oldtime=$(date '+%s')
        fi
    fi

    if [ "$curstate" == "LOCK" ]
    then
            curtime=$(date '+%s')
            timediff=$(($curtime - $oldtime))
            if [ $timediff -gt $timeout ]
            then
                echo 1 | sudo /usr/libexec/qubes/dom0-dms-activate
            fi
    fi
done
