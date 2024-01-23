from datetime import timedelta
import requests
freetrail = timedelta(seconds=7)

localIP = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
# TODO error checking