import subprocess
import os

from random import randint, choice
from utils.util_sys import XRAY_PATH
from utils.util_json import getPubkey
from server.models import addUserToDB, addShortidsToDB

def generateAdmin(clientNum=1):
    uuid = generateUUID()
    shortids = [generateShortID() for i in range(clientNum)]
    port = 443 #generatePort()
    pubkey, prikey = generateKey()
    return uuid, shortids, port, pubkey, prikey

def generateUser(clientNum=1):
    uuid = generateUUID()
    shortids = [generateShortID() for i in range(clientNum)]
    port = 443 #generatePort()
    pubkey = getPubkey()
    return uuid, shortids, port, pubkey

def generatePort():
    port = randint(10000, 30000) #TODO:check repeated
    return port

def generateUUID():
    output, error = subprocess.Popen([XRAY_PATH, 'uuid'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error:
        print("Error: unable to generate uuid")
    uuid = output.decode()
    return uuid[:-1] # remove \n at the end

def generateKey():
    output, error = subprocess.Popen([XRAY_PATH, 'x25519'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if error:
        print("Error: unable to generate reality key")

    key = output.decode()
    prikey, pubkey = key[13:56], key[69:-1]
    return pubkey, prikey

def generateShortID():
    shortid = ''.join(choice('0123456789abcdef') for _ in range(16))
    return shortid

