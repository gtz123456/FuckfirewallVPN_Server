from datetime import timedelta
import requests
freetrail = timedelta(seconds=7)

requests.packages.urllib3.util.connection.HAS_IPV6 = False # force ipv4
localIP = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
# TODO error checking