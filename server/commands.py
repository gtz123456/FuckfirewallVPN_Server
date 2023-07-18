import click

from server import app, db
from server.models import User, GiftCard, Service
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
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
def init():
    db.drop_all()
    db.create_all()
    email = input('Input admin email:')
    print(email)
    password = input('Input admin password:')
    print(password)
    uuid, shortids, port, pubkey, prikey = generateAdmin()
    addUserToDB(email, password, uuid, pubkey, 0)
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
    pubkey = getPubkey()
    addUserToDB(email, password, None, pubkey, 0) # TODO：check repeated email

@app.cli.command()
def addService():
    email = input('Input email:')
    user = User.query.filter_by(email=email).first()
    uuid, shortids, port, pubkey = generateUser()
    user.uuid = uuid
    addShortidsToDB(uuid, shortids)
    db.session.commit()
    from utils.util_json import loadConfigToJSON
    loadConfigToJSON()

@app.cli.command()
def printusers():
    users = User.query.all()
    for user in users:
        print(user.id, user.email)