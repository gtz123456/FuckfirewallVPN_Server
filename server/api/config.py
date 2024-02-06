from flask import jsonify, g
from server import app, db
from server.api.auth import token_auth
from server.models import User, ShortID
from datetime import datetime, timedelta

from utils.util_static import localIP

@app.route('/api/config', methods=['GET'])
@token_auth.login_required
def getConfig():
    user = token_auth.current_user
    port = 443
    shortidItem = ShortID.query.filter_by(uuid=user.uuid).first()
    shortid = shortidItem.shortid if shortidItem else ''
    ip = localIP
    url = "vless://{user.uuid}@{ip}:{port}?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.amazon.com&fp=chrome&pbk={user.pubkey}&sid={shortid}&type=tcp&headerType=none#la"
    return jsonify({'uuid': user.uuid, 'port': port, 'pubkey': user.pubkey, 'shortid': shortid, 'balance': user.balance, 'expireOn': user.expireOn.strftime('%Y-%m-%d %H:%M'), 'referralCode': user.id, 'url': url.format(user=user, ip=ip, shortid=shortid, port=port)})

@app.route('/api/addPlan', methods=['GET'])
@token_auth.login_required
def addPlan():
    user = User.query.filter_by(uuid=token_auth.current_user.uuid).first()
    user.expireOn = user.expireOn + timedelta(days=30)
    db.session.commit()
    # activate user(by reloading config)
    from utils.util_json import loadConfigToJSON
    loadConfigToJSON()
    from utils.util_sys import xrayRestart
    xrayRestart(app.xrayProcess.pid)
    return jsonify({'result': True})