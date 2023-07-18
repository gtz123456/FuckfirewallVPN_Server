import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XRAY_PATH = os.path.join(BASE_DIR, '../xray', 'xray')

def proxyOn():
    setSocks = f'networksetup -setsocksfirewallproxy networkservices 127.0.0.1 1081'
    os.popen(setSocks)

    sethttp = f'networksetup -setwebproxy networkservices 127.0.0.1 1081'
    os.popen(sethttp)

    proxyOn = 'networksetup -setsocksfirewallproxystate Wi-Fi on'
    os.popen(proxyOn)

def proxyOff():
    proxyOff = 'networksetup -setsocksfirewallproxystate Wi-Fi off'
    os.popen(proxyOff)

def xrayOn():
    xrayProcess = subprocess.Popen([os.path.join(BASE_DIR, '..', 'xray', 'xray')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return xrayProcess

def xrayOff(pid):
    os.popen('kill ' + str(pid))

def xrayRestart(pid):
    xrayOff(pid)
    return xrayOn()
