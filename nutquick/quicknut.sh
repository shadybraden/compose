#!/bin/bash

# this sends shutdown when the battery is at 50%

# check ups status and battery %
BATTERY_LEVEL=$(upsc holmie@192.168.50.65 battery.charge)
UPS_STATUS=$(upsc holmie@192.168.50.65 ups.status)
SHUTDOWN_PERCENT=50
DEVICE_TAG=house

if [ "$UPS_STATUS" != OL ]; then # if not online
        # Check if UPS is on battery and if battery charge is less than 90 and isnt charging
        if [ "$UPS_STATUS" != "OL CHRG" ]; then # if not charging
                if [ "$BATTERY_LEVEL" -lt "$SHUTDOWN_PERCENT" ]; then
                        # if less than the number, ntfy then shutdown in 1 minute
                        curl -H "Tags: $DEVICE_TAG,bangbang" -H "Priority: high" -H "X-Title:HOLMIE SHUTTING DOWN" -d "" https://ntfy.holmlab.org/UPSuWd9jG23WS ; /sbin/shutdown -h +1
                fi
        fi
        if [ "$UPS_STATUS" = "OL CHRG" ]; then
                curl -H "Tags: battery,arrow_up" -H "Priority: min" -H "X-Title: UPS charging (at "$BATTERY_LEVEL"%)" -d "" https://ntfy.holmlab.org/UPSuWd9jG23WS
        fi
fi

if [ "$UPS_STATUS" = RB ]; then # replace battery?
        # NTFY if replacement battery
        curl -H "Tags: battery" -H "Priority: min" -H "X-Title: Replace UPS battery" -d "" https://ntfy.holmlab.org/UPSuWd9jG23WS
fi
