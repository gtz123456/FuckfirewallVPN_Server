import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XRAY_PATH = os.path.join(BASE_DIR, '../xray', 'xray')

def xrayOn():
    xrayProcess = subprocess.Popen([os.path.join(BASE_DIR, '..', 'xray', 'xray')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return xrayProcess

def xrayOff(pid):
    os.popen('kill ' + str(pid))

def xrayRestart(pid):
    xrayOff(pid)
    return xrayOn()
