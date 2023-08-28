from flask import jsonify, request
from server import app
from server.models import User

@app.route('/api/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    refer = request.form['refer']
    return jsonify({'result': User.register(email, password, refer)})