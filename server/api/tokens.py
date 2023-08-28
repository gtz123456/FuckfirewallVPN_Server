from flask import jsonify, g
from server import app
from server.api.auth import basic_auth

@app.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.currentUser.getToken()
    from server import db
    db.session.commit()
    return jsonify({'token': token})