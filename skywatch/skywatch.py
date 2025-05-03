import json
import requests
from datetime import datetime, timedelta

# download data
url = 'https://adsb.holmlab.org/data/aircraft.json'
response = requests.get(url)
# Save the content to a file
with open('data.json', 'w') as f:
    f.write(response.text)

# CHECK recents.txt for old hexes
now = datetime.now()
time_threshold = now - timedelta(minutes=5) # old > 5 minutes
# Read and filter lines
filtered_lines = []
with open('recents.txt', 'r') as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) >= 2:
            timestamp_str = f"{parts[1]} {parts[2]}"
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                if timestamp >= time_threshold:
                    filtered_lines.append(line)
            except ValueError:
                # Skip lines with invalid timestamp format
                continue
# Write the filtered lines back to the file
with open('recents.txt', 'w') as file:
    file.writelines(filtered_lines)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# fetch relevent info for each craft
with open('data.json', 'r') as file:
    data = json.load(file)
for ac in data.get('aircraft', []):
    hex_value = ac.get('hex', 'unknown') # hex or icao  
    desc_value = ac.get('desc', 'unknown') # long description of aircraft
    short_type_value = ac.get('t', 'unknown') # short description of aircraft
    registration = ac.get('r', 'unknown')
    ownOp_value = ac.get('ownOp', 'unknown') # owner
    r_dst_value = ac.get('r_dst', 'unknown') # distance form antenna
    r_dst_value = str(r_dst_value)
    dbFlags = ac.get('dbFlags', '0') # 1=MILLITARY 8=LADD 0=rando
    dbFlags = int(dbFlags)

    # set vars for message:
    title = "watchlist | " + r_dst_value + " away"
    message = ownOp_value + '\n' + desc_value + " | " + short_type_value + '\n' + "https://adsb.holmlab.org/?icao=" + hex_value
    click = "https://adsb.lol/?zoom=11&SiteLat=42.587&SiteLon=-71.377&icao=" + hex_value

    if dbFlags == 0: # if not millitary, check watchlist.txt
        with open("watchlist.txt", "r") as file:
            for line in file:
                if line.strip()[:6].lower() == hex_value:
                    #print("On Watchlist", line.strip())
                    send_message = 1
                    break
            else:
                #print("NOT on watchlist")
                send_message = 0
    if dbFlags == 1:
        title = "MILLITARY | " + r_dst_value + " away"
        send_message = 1
    if dbFlags == 8:
        title = "LADD | " + r_dst_value + " away"

    # check recents.txt for current hex
    # if match, send_message = 0
    try:
        with open("recents.txt", "r") as file:
            #send_message = 1  # default to sending unless a match is found
            for line in file:
                if line[:6].lower() == hex_value.lower():
                    # Match found
                    send_message = 0
                    break
    except FileNotFoundError:
        print("Error: recents.txt not found.")
    except Exception as e:
        print("An error occurred:", str(e))

    # Current timestamp in the desired format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Write to file
    if send_message == 1:
        with open("recents.txt", "a") as file:
            file.write(f"{hex_value} {timestamp}\n")

    if send_message == 0:
        printTime = datetime.now().strftime("%HH:%M:%S")
        print(printTime, ":", hex_value, "no ntfy")

    if send_message == 1:
        print(title)
        print(message)
        ntfy_url="https://ntfy.holmlab.org/adsbGMzCPurvWR4ZSE8u98EQWGj6Eezdw4fr"
        requests.post(ntfy_url,
            data=(message),
                headers={
                    "Title": title,
                    "Click": click,
                    "Priority": "low",
        })