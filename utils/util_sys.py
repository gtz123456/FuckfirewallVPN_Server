import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XRAY_PATH = os.path.join(BASE_DIR, '../xray', 'xray')

PLATFORM = sys.platform
if PLATFORM.startswith('win'):
    PLATFORM = 'windows'
elif PLATFORM == 'darwin':
    PLATFORM = 'macos'
else:
    PLATFORM = 'linux'

def xrayOn():
    fileName = 'xray.exe' if PLATFORM == 'windows' else 'xray_linux'
    xrayProcess = subprocess.Popen([os.path.join(BASE_DIR, '..', 'xray', fileName)], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return xrayProcess

def xrayOff(pid):
    os.popen('kill ' + str(pid))

def xrayRestart(pid):
    xrayOff(pid)
    return xrayOn()
