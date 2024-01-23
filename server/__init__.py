import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# solve cross origin problem
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from server.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from server.models import User
    user = User.query.first()
    return dict(user=user)

from utils.util_sys import BASE_DIR
from server import commands
# from server import views, errors, commands 
# remove this to transfer to api

import server.api

if sys.argv[0] != 'flask' or sys.argv[1] == 'run':
    print('Turning on xray-core')
    from utils.util_sys import xrayOn
    app.xrayProcess = xrayOn()
    print("pid", app.xrayProcess.pid)
    from utils.util_supervisor import Supervisor
    supervisor = Supervisor(app)