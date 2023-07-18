import json
import os

from utils.util_sys import BASE_DIR, XRAY_PATH
from server.models import User, ShortID

def initRealityClientConfig(address: str, port: int, uuid: str, pubkey: str, shortid: str):
    with open(os.path.join(BASE_DIR, 'utils', 'defaultClient.json')) as file:
        data = json.load(file)

    settings = data['outbounds'][0]['settings']
    vnext = settings['vnext'][0]
    vnext['address'] = address
    vnext['port'] = port

    user = vnext['users'][0]
    user['id'] = uuid

    streamSettings = data['outbounds'][0]['streamSettings']
    realitySettings = streamSettings['realitySettings']
    realitySettings['publicKey'] = pubkey
    realitySettings['shortId'] = shortid

    with open(os.path.join(BASE_DIR, 'xray', 'config.json'), mode='w+') as file:
        json.dump(data, file)

def initRealityServerConfig(port: int, uuid: str, prikey: str, shortid: str):
    with open(os.path.join(BASE_DIR, 'defaultServer.json')) as file:
        data = json.load(file)

    inbound = data['inbounds'][0]
    inbound['port'] = port

    client = inbound['settings']['clients'][0]
    client['id'] = uuid

    realitySettings = data['inbounds'][0]['streamSettings']['realitySettings']
    realitySettings['privateKey'] = prikey
    realitySettings['shortIds'] = [shortid]

    with open(os.path.join(BASE_DIR, '../xray', 'config.json'), mode='w+') as file:
        json.dump(data, file)


def loadConfigToJSON():
    with open(os.path.join(BASE_DIR, '../xray', 'config.json')) as file:
        data = json.load(file)

    # reload uuid
    from server.models import User, ShortID
    uuids = User.query.with_entities(User.uuid)
    data['inbounds'][0]['settings']['clients'] = []
    for uuid in uuids:
        if uuid[0]:
            data['inbounds'][0]['settings']['clients'].append({'id':uuid[0], 'flow': 'xtls-rprx-vision'})

    # reload shortid
    shortids = ShortID.query.with_entities(ShortID.shortid)
    data['inbounds'][0]['streamSettings']['realitySettings']['shortIds'] = []
    for shortid in shortids:
        data['inbounds'][0]['streamSettings']['realitySettings']['shortIds'].append(shortid[0])

    with open(os.path.join(BASE_DIR, '../xray', 'config.json'), mode='w+') as file:
        json.dump(data, file)

def getPubkey():
    pubkey = User.query.filter_by(id=1).with_entities(User.pubkey).first().pubkey
    return pubkey

