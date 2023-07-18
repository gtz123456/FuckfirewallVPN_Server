import subprocess
import os
from time import sleep
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
subprocess.Popen([os.path.join(BASE_DIR, '..', 'xray', 'xray')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
sleep(1000000)