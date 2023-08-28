import click

from datetime import timedelta

from server import app, db
from server.models import User, ShortID
from utils.util_configure import generateAdmin, generateUser
from utils.util_json import initRealityServerConfig
from server.models import addShortidsToDB, addUserToDB

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def init():
    db.drop_all()
    db.create_all()

    email = input('Input admin email:')
    password = input('Input admin password:')
    uuid, shortids, port, pubkey, prikey = generateAdmin()

    addUserToDB(email, password, uuid, pubkey, 0, trailtime=timedelta(days=365))
    addShortidsToDB(uuid, shortids)
    initRealityServerConfig(port, uuid, prikey, shortids[0])

@app.cli.command()
def addUser():
    email = input('Input email:')
    repeated = User.query.filter_by(email=email).all()
    if repeated:
        print('Repeated email!')
        return
    password = input('Input password:')

    from utils.util_json import getPubkey
    uuid, shortids, port, pubkey = generateUser()
    addUserToDB(email, password, uuid, pubkey, 2, referee=0)
    addShortidsToDB(uuid, shortids)

@app.cli.command()
def addPlan():
    email = input('Input email:')
    user = User.query.filter_by(email=email).first()
    uuid, shortids, port, pubkey = generateUser()
    user.uuid = uuid
    addShortidsToDB(uuid, shortids)
    db.session.commit()
    from utils.util_json import loadConfigToJSON
    loadConfigToJSON()

@app.cli.command()
def printUsers(): 
    users = User.query.all()
    for user in users:
        print(user.id, user.email, user.balance)

@app.cli.command()
def printshortids(): 
    shortids = ShortID.query.all()
    for shortid in shortids:
        print(shortid.id, shortid.uuid, shortid.shortid)

@app.cli.command()
@click.option('--uuid', prompt=True, help='The uuid to delete.')
def deleteShortids(uuid): 
    from server.models import removeShortidsFromDB
    removeShortidsFromDB(uuid)