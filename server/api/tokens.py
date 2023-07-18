from flask import jsonify, g
from server import app
from server.api.auth import basic_auth, token_auth
from server.models import ShortID

@app.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.currentUser.getToken()
    from server import db
    db.session.commit()
    return jsonify({'token': token})

@app.route('/api/config', methods=['GET'])
@token_auth.login_required
def get_config():
    user = token_auth.current_user
    shortid = ShortID.query.filter_by(uuid=user.uuid).first().shortid
    return jsonify({'uuid': user.uuid, 'port': 443, 'pubkey': user.pubkey, 'shortid': shortid})