import json
import requests
from datetime import datetime, timedelta
send_message = 0
priority = 'low'

print("-=-=-=-=-=-=-=-=-=-=-=-=-")

# download data
do_download = 1
if do_download == 1:
    url = 'https://adsb.holmlab.org/data/aircraft.json'
    response = requests.get(url)
    # Save the content to a file
    with open('data.json', 'w') as f:
        f.write(response.text)

# CHECK recents.txt for old hexes
now = datetime.now()
time_threshold = now - timedelta(minutes=10) # old > 5 minutes
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
    short_type_value = ac.get('t', 'unknown') # short description of aircraft (ie A337)
    short_type_value = str(short_type_value)
    registration = ac.get('r', 'unknown')
    ownOp_value = ac.get('ownOp', 'na') # owner
    r_dst_value = ac.get('r_dst', 'na') # distance form antenna
    r_dst_value = str(r_dst_value)
    dbFlags = ac.get('dbFlags', '0') # 1=MILLITARY 8=LADD 0=rando
    dbFlags = int(dbFlags)
    alt_baro= ac.get('alt_baro', '0')
    alt_baro = str(alt_baro)
    squawk = ac.get('squawk', 'unknown')
    squawk = str(squawk)

    # set vars for message:
    title = "WATCH | " + short_type_value + " | " + desc_value
    message = r_dst_value + " mi | " + "alt:" + alt_baro + ownOp_value +'\n' + "https://adsb.holmlab.org/?icao=" + hex_value
    click = "https://adsb.lol/?zoom=11&icao=" + hex_value

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
        send_message = 1

    if send_message == 1: # if we are planning on sending, check if alt_baro == "0", fetch from public site
        if alt_baro == "0":
            public_url = f'https://opendata.adsb.fi/api/v2/hex/{hex_value}'
            try:
                print("requesting altitude from opendata.adsb.fi for:", hex_value)
                public_response = requests.get(public_url)
                public_response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
                
                # Attempt to parse the response as JSON
                data = public_response.json()
                
                # Extract alt_baro from the JSON response
                alt_baro = data['ac'][0]['alt_baro'] if 'ac' in data and len(data['ac']) > 0 else None
                alt_baro = str(alt_baro)
                
                # Print the response in a readable format
                # print("Public Response:", json.dumps(data, indent=4))
                print("Public Altitude (alt_baro):", alt_baro)
                
            except requests.exceptions.RequestException as e:
                print("Error fetching data:", e)
            except json.JSONDecodeError:
                print("Error decoding JSON response")

    if dbFlags == 1:
        title = "MILL | " + short_type_value + " | " + desc_value
        send_message = 1
    if dbFlags == 8:
        title = "LADD | " + short_type_value + " | " + desc_value
    
    # set ntfy priority based on altitiude
    alt_baro = int(alt_baro)
    if alt_baro >= 2000:
        priority = 'low'
    if alt_baro <= 2000:
        priority = 'default'
    if alt_baro >= 10000:
        priority = 'min'
    # print("alt:", alt_baro, priority)
    alt_baro = str(alt_baro)

    if short_type_value in ["HAWK", "EUFI", "RFAL", "A124", "A140", "A148", "A158", "A225", "A225", "BLCF", "CL2T", "AN12", "AN24", "AN26", "AN28", "AN30", "AN32", "AN72", "B52", "PRTS", "F35", "U2", "HRON", "SLCH", "WB57", "Q9", "Q4", "C2", "B70", "W135", "B1", "B742", "R135", "E2", "3B4", "E6", "F16", "E3TF"]: # https://en.wikipedia.org/wiki/List_of_aircraft_type_designators
        send_message = 1
        priority = 'default'
    
    if squawk == "7500":
        send_message = 1
        priority = 'max'
        title = "HIJACK | " + short_type_value + " | " + desc_value
    if squawk == "7600":
        send_message = 1
        priority = 'default'
        title = "Radio Failure | " + short_type_value + " | " + desc_value
    if squawk == "7700":
        send_message = 1
        priority = 'default'
        title = "Emergency | " + short_type_value + " | " + desc_value

    if send_message == 1: # if we are planning on sending, check ignorelist
        with open("ignorelist.txt", "r") as file:
            for line in file:
                if line.strip()[:6].lower() == hex_value:
                    print(line.strip(), "On ignorelist")
                    send_message = 0
                    break

    # check recents.txt for current hex
    # if match, send_message = 0
    try:
        with open("recents.txt", "r") as file:
            #send_message = 1  # default to sending unless a match is found
            for line in file:
                if line[:6].lower() == hex_value.lower(): # only check first 6 characters of the line
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
        printTime = datetime.now().strftime("%I:%M %p")
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
                    "Priority": priority,
        })
