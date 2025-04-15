# Proxy

Runs several types of proxy: HTTP, Shadowsocks and socks5

For the script:
`cp restart_proxy.sh.sample restart_proxy.sh`
`chmod +x restart_proxy.sh`
To make run on a schedule:
`sudo su`
`crontab -e`
`0 6 * * * /home/user/homelab/docker/proxy/restart_proxy.sh` - for daily at 6am

This will work without the script. The script is just to automate restarting of the containers to get a new IP on a schedule. 
Line 6 and below are not required.

https://github.com/qdm12/gluetun?tab=readme-ov-file#setup
https://github.com/serjs/socks5-server?tab=readme-ov-file#examples