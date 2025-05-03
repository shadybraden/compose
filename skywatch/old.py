import re
import os
import time
import requests
# curl https://opendata.adsb.fi/api/v2/hex/ae0582


# 1 to send message via ntfy
actually_send_message = 1
# 1 to download. anything else to skip
do_download_live_data = 1
# 1 to skip extra notificaions
double_send = 1


# set absolute path to folder:
#absolute_path="/home/shady/Documents/skywatch/"
absolute_path="/home/holmie/skywatch/"


sent = 0
hex = ""
reg = ""
desc = ""
title = ""
owner = ""
dbFlags = ""
last_hex = ""
send_message = 0
aircraft_type = ""
craft_distance = ""
title = "Aircraft!"
keyword=absolute_path + "keywords.txt"
aircraft=absolute_path + "aircraft.csv"
watchlist=absolute_path + "watchlist.txt"
live_data=absolute_path + "live_data.json"
public_icao_link="https://adsb.lol/?zoom=11&SiteLat=42.587&SiteLon=-71.377&icao="
last_hex_file=absolute_path + "last_hex.txt"
icao_link="https://adsb.holmlab.org/?icao="
testing_json=absolute_path + "snapsnot_of_live_data.json"
get_data_url="https://adsb.holmlab.org/data/aircraft.json"
ntfy_url="https://ntfy.holmlab.org/adsbGMzCPurvWR4ZSE8u98EQWGj6Eezdw4fr"

# download data from get_data_url (my live antenna)
if do_download_live_data == 1:
    def download_data(url, file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            #print(f"Downloaded data to {file_path}")
        #else:
            #print(f"Error: {response.status_code}")
    download_data(get_data_url, live_data) 

# delete first 3 lines from live_data and last 2 lines (if the word "now" is in the chars 3-6 of line 1) (and quotes)
if sent == 0:
    with open(live_data, "r") as f:
        data = f.read()
        if len(data) >= 6:  # make sure we have enough characters to check
            if data[3] == 'n' and data[4] == 'o' and data[5] == 'w':
                #print("the now from live_data is there - deleteing")
                with open(live_data, 'r') as f:
                    lines = f.readlines()
                del lines[:3]  # delete the first 3 lines
                del lines[-2:]  # delete the last 2 lines
                with open(live_data, 'w') as f:
                    f.writelines(lines)
    # delete all quotations from live_data
    # Open the file in read mode
    with open(live_data, "r") as f:
        # Read the contents of the file
        content = f.read()
    # Remove all quote marks from the content
    content = content.replace('"', "").replace("'", "")
    # Open the file in write mode and write the modified content
    with open(live_data, "w") as f:
        f.write(content)

# edit the file so every aircraft takes up one line of the file
#print(live_data)
if sent == 0:
    lines = []
    with open(live_data, 'r') as f:
        for line in f.readlines():
            lines.append(re.sub(r'\n\s*(}\Z|$)', '', line.strip()))
    with open(live_data, 'w') as f:
        f.write(''.join(lines))

    with open(live_data, "r+") as f:
        content = f.read()
        new_content = ""
        for char in content:
            if char == "}":
                new_content += char + "\n"
            else:
                new_content += char
        f.seek(0)
        f.write(new_content)

# for each line in the file live_data, get the "r" and "hex" and "dbFlags" and "dist"
with open(live_data, "r") as file:
    for line in file:
        if "hex:" in line:                            # find hex
            index = line.index("{hex:")
            hex_index = index + 5 # value to shift from first char of search
            hex = line[index+5:index+len(line)-1].split(",",1)[0] # get data from searched term to next comma
        try:
            if "r:" in line:                              # find registration
                index = line.index(",r:")
                reg_index = index + 3
                reg = line[index+3:index+len(line)-1].split(",",1)[0]
        except ValueError:
            pass
        # adding searching for `r_dst` to see how far away an aircraft is:
        try:
            if "r_dst" in line:                         # find dbFlags
                index = line.index(",r_dst")
                craft_distance_index = index + 8
                craft_distance = line[index+7:index+len(line)-1].split(",",1)[0]
                #send_message = 1
                #print(craft_distance)
            else:
                craft_distance = "NA"
        except ValueError:
            pass
        if "dbFlags" in line:                         # find dbFlags
            index = line.index(",dbFlags")
            dbFlags_index = index + 8
            dbFlags = line[index+9:index+len(line)-1].split(",",1)[0]
            #send_message = 1
            #print(dbFlags)
        try:  
            if "t:" in line:                              # find type of aircraft
                index = line.index(",t:")
                type_index = index + 3
                aircraft_type = line[index+3:index+len(line)-1].split(",",1)[0]
        except ValueError:
            pass
        if ",desc:" in line:                              # find description of aircraft
            index = line.index(",desc:")
            desc = line[index+6:index+len(line)-1].split(",",1)[0] 
        if dbFlags == "1":
            title = "MILLITARY Aircraft!"
            send_message = 1
        if dbFlags == "8":
            title = "LADD Aircraft!"
        title = title + " | " + craft_distance + " Miles away"
    
        # compare against watchlist.txt for reg
        with open(watchlist, 'r') as f:
            watchlist_lines = [line.strip() for line in f.readlines()]
        if reg.lower() in [line.lower().strip() for line in watchlist_lines]:
            #print("reg match in watchlist")
            send_message = 1
        #else:
            #print("no reg matches")
        # compare against watchlist.txt for hex
        with open(watchlist, 'r') as f:
            watchlist_lines = [line.strip() for line in f.readlines()]
        if hex.lower() in [line.lower().strip() for line in watchlist_lines]:
            #print("hex match in watchlist")
            send_message = 1
        #else:
            #print("no hex matches")
        
        # if send_message = 1 then search for the reg in aircraft.csv for the owner
        # to get notified about more aircraft, add its icao or hex or registration or n-number to the watchlist.txt
        if send_message == 1:
            with open(aircraft, 'r') as file:
                for line in file:
                    if reg in line:
                        parts = line.strip().split(';')
                        owner = parts[-2].strip()

        #print("hex:", hex)
        #print("reg:", reg)
        #print("dbFlags:", dbFlags)
        #print(owner)
        #print("-------------------")

        local_link = icao_link + hex
        public_link = public_icao_link + hex
        local_md = "[local_link]" + "(" + local_link + ")"
        public_md = "[public_link]" + "(" + public_link + ")"

        message = owner + " | desc: " + desc + " | type: " + aircraft_type  + '\n' + reg + '\n' + local_link

        # read file for the last hex send thru ntfy
        if send_message == 1:
            with open(last_hex_file, 'r') as f:
                last_hex = f.read()
        # if the previous hex and current one match, dont send message
        if double_send == 1:
            if last_hex == hex:
                send_message = 0

        # actually send the message
        if actually_send_message == 1:
            if send_message == 1:
                requests.post(ntfy_url,
                    data=(message),
                        headers={
                            "Title": title,
                            "Click": public_link,
                            "Priority": "low",
                            "Markdown": "yes",
                })
                sent = 1
        # write current value of hex to the file for next line of file or next run of script
        if send_message == 1:
            with open(last_hex_file, 'w') as f:
                f.write(hex)

        # reset for next line in live_data
        hex = ""
        reg = ""
        dbFlags = ""
        owner = ""
        send_message = 0
        #time.sleep(0.1)
