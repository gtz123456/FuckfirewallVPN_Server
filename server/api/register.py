from flask import jsonify, request
from server import app
from server.models import User

@app.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')['_value']
    password = request.json.get('password')['_value']
    refer = request.json.get('refer')
    return jsonify({'result': User.register(email, password, refer)})