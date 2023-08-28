from flask import jsonify, g
from server import app
from server.api.auth import token_auth
from server.models import ShortID
from datetime import datetime

@app.route('/api/config', methods=['GET'])
@token_auth.login_required
def get_config():
    user = token_auth.current_user

    shortidItem = ShortID.query.filter_by(uuid=user.uuid).first()
    shortid = shortidItem.shortid if shortidItem else ''
    print(user.expireOn)
    return jsonify({'uuid': user.uuid, 'port': 443, 'pubkey': user.pubkey, 'shortid': shortid, 'balance': user.balance, 'expireOn': user.expireOn.strftime('%Y-%m-%d %H:%M'), 'referralCode': user.id})