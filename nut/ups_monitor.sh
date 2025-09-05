#!/bin/bash

# script for reporting the status of a NUT UPS

#!/bin/bash

# this sends shutdown when the battery is at 90%

# check ups status and battery %
BATTERY_LEVEL=$(upsc holmie@192.168.50.65 battery.charge)
UPS_STATUS=$(upsc holmie@192.168.50.65 ups.status)
UPS_RUNTIME=$(upsc holmie@192.168.50.65 battery.runtime)


if [ "$UPS_STATUS" == OL ] && [ "$BATTERY_LEVEL" == 100 ]; then # if online, and charged
        echo "$(date): ups online, at ${BATTERY_LEVEL}%"
else
        echo "UPS doing something"
        curl -H "Tags: battery" -H "Priority: default" -H "X-Title: UPS at ${BATTERY_LEVEL}%" -d "status: ${UPS_STATUS} | runtime: ${UPS_RUNTIME}" https://ntfy.holmlab.org/UPSuWd9jG23WS
fi
