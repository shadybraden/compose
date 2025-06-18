#!/bin/bash

# this runs when the battery is at 90%

# check ups status and battery %
BATTERY_LEVEL=$(upsc pi3@192.168.50.61 battery.charge)
UPS_STATUS=$(upsc pi3@192.168.50.61 ups.status)
SHUTDOWN_PERCENT=90
DEVICE_TAG=desktop_computer

if [ "$UPS_STATUS" != OL ]; then # if not online
        # Check if UPS is on battery and if battery charge is less than 90 and isnt charging
        if [ "$UPS_STATUS" != "OL CHRG" ]; then # if not charging
                if [ "$BATTERY_LEVEL" -lt "$SHUTDOWN_PERCENT" ]; then
                        # if less than the number, ntfy then shutdown in 1 minute
                        curl -H "Tags: $DEVICE_TAG,bangbang" -H "Priority: high" -H "X-Title: SHADYPC SHUTTING DOWN" -d "" https://ntfy.holmlab.org/UPSuWd9jG23WS ; /sbin/shutdown -h +1
                fi
        fi
fi
