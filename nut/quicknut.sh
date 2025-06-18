#!/bin/bash

# this sends shutdown when the battery is at 90%

# check ups status and battery %
BATTERY_LEVEL=$(upsc holmie@192.168.50.65 battery.charge)
UPS_STATUS=$(upsc holmie@192.168.50.65 ups.status)
SHUTDOWN_PERCENT=90
DEVICE_NAME=$(uname -n)

if [ "$UPS_STATUS" == OL ]; then # if online
        echo "$(date): ups online, at ${BATTERY_LEVEL}%"
else
        echo "OFFLINE!"
        if [ "$BATTERY_LEVEL" -lt "$SHUTDOWN_PERCENT" ]; then
                echo "SHUTDOWN SOON sending ntfy"
                curl -H "Tags: bangbang" -H "Priority: high" -H "X-Title: 90% SHUTDOWN" -d "${DEVICE_NAME}" https://ntfy.holmlab.org/UPSuWd9jG23WS
                echo "ntfy sent. SHUTTING DOWN IN 1 MINUTE"
                /sbin/shutdown -h +1 # shutdown in ***1 MINUTE***
                # cancel with: sudo shutdown -c
        fi
fi
