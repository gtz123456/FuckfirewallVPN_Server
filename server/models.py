import base64
import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from server import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    privilege = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    referee = db.Column(db.Integer)
    uuid = db.Column(db.String(36), index=True, unique=True)
    pubkey = db.Column(db.String(43))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

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

class GiftCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    amount = db.Column(db.Integer)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ServiceOwner = db.Column(db.Integer)
    ServiceType = db.Column(db.Integer)
    ServiceStartat = db.Column(db.DateTime)
    ServiceEndat = db.Column(db.DateTime)
    ServiceBandwith = db.Column(db.Integer)
    ServiceData = db.Column(db.Integer) # 
    ServiceRenewal = db.Column(db.Integer) # count by day

class ShortID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    shortid = db.Column(db.String(16))

def addUserToDB(email, password, uuid, pubkey, privilege, balance=0, referee=0):
    user = User(email=email, uuid=uuid, pubkey=pubkey, privilege=privilege, balance=balance, referee=referee)
    user.setPassword(password)
    db.session.add(user)
    db.session.commit()

def addShortidsToDB(uuid, shortids):
    '''Used to activate user'''
    for shortid in shortids:
        db.session.add(ShortID(uuid=uuid, shortid=shortid))
    db.session.commit()
