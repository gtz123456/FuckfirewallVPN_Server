import base64
import os
import re

from datetime import datetime
from flask_login import UserMixin
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from server import db

from utils.util_static import freetrail

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    privilege = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    referee = db.Column(db.Integer) # referee's id
    uuid = db.Column(db.String(36), index=True, unique=True)
    pubkey = db.Column(db.String(43))

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    bandwith = db.Column(db.Integer)
    traffic = db.Column(db.Integer)
    expireOn = db.Column(db.DateTime)
    billingCycle = db.Column(db.Integer) # count by day

    def getToken(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token

    def revokeToken(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()

    @staticmethod
    def checkToken(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    
    @staticmethod
    def register(email, password, refer=0):
        if not email:
            return 'Empty email.'
        if not password:
            return 'Empty password.'

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if len(email) >= 128 or not re.match(pattern, email):
            return 'Invalid email.'

        repeated = User.query.filter_by(email=email).all()
        if repeated:
            return 'Email exist'

        from utils.util_configure import generateUser
        uuid, shortids, port, pubkey = generateUser()

        addUserToDB(email, password, uuid, pubkey, 2, referee=refer)

        addShortidsToDB(uuid, shortids)
        
        return 'Register success.'
    
    @staticmethod
    def login(email, password):
        if not email:
            return 'Empty email.'
        if not password:
            return 'Empty password.'

        user = User.query.filter_by(email=email).first()
        if not user:
            return 'Email not registered.'
        
        if email == user.email and user.validatePassword(password):
            login_user(user)
            return 'Login success.'

        return 'Invalid username or password.'

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def validatePassword(self, password):
        return check_password_hash(self.password_hash, password)
    
    def setPrivilege(self, privilege):
        self.privilege = privilege
        db.session.commit()

    def getBalance(self):
        return self.balance

    def setBalance(self, amount):
        self.balance = amount
        db.session.commit()

    def rechargeBalance(self, amount):
        self.balance += amount
        db.session.commit()

class ShortID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True)
    shortid = db.Column(db.String(16))

def addUserToDB(email, password, uuid, pubkey, privilege, balance=0, referee=0, trailtime=freetrail):
    user = User(email=email, uuid=uuid, pubkey=pubkey, privilege=privilege, balance=balance, referee=referee, bandwith=float('inf'), traffic=float('inf'), expireOn=datetime.utcnow() + trailtime)
    user.setPassword(password)
    db.session.add(user)
    db.session.commit()

def addShortidsToDB(uuid, shortids):
    '''Used to activate user'''
    for shortid in shortids:
        db.session.add(ShortID(uuid=uuid, shortid=shortid))
    db.session.commit()

def removeShortidsFromDB(uuid):
    for shortid in ShortID.query.filter_by(uuid=uuid).all():
        db.session.delete(shortid)
    db.session.commit()