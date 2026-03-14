# Plane Tracking and alerting

This Project is a complete system for scanning and alerting for interesting Millitary aircraft, Police helicopters, weird NASA cargo planes and much more.

It uses a python program, `skywatch.py` that pulls data from my API run by Ultrafeeder (see ADSB folder). Ultrafeeder is connected via usb to a SDR to an antenna tuned to 1090 MHz. This setup give me a nice web interface and the aforementioned API that shows the nearby aircraft. The python program then sends a custom notification to my phone via NTFY, the notification server I also run. 

The notification comes through with various pices of information, such as the altitude (lower = better photos :) ), type of aircraft, distance away and the owner of the aircraft. 

The python program is wrapped into a docker image, bundled with the ignore list, watchlist and the functionality to keep track of recently alerted aircraft. This allows Komodo to easily schedule and manage Skywatch.