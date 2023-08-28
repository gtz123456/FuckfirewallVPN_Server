from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from server import app, db
from server.models import User, addUserToDB

import re

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settingsPage():
    if not current_user.is_authenticated:
        return redirect(url_for('settingsPage'))
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'password':
            password = request.form['password']
            if not password:
                flash('Empty password.')
                return redirect(url_for('settingsPage'))
            current_user.setPassword(password)
            db.session.commit()
            flash('Password updated.')
            return redirect(url_for('settingsPage'))
        elif form_type == 'recharge':
            amount = request.form['amount']

            # input checking
            if not amount:
                flash('Empty amount.')
                return redirect(url_for('settingsPage'))
            
            if len(amount) < 10 and amount.isdigit():
                amount = int(amount)
            else:
                flash('Amount invalid')
                return redirect(url_for('settingsPage'))
            
            current_user.rechargeBalance(amount)
            flash('Balance updated.')
            return redirect(url_for('settingsPage'))

    balance = current_user.getBalance()
    return render_template('settings.html', balance=balance)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        refer = request.form['refer']

        registerMessage = User.register(email, password, refer)
        flash(registerMessage)
        if registerMessage == 'Register success.':
            user = User.query.filter_by(email=email).first()
            login_user(user)
            return redirect(url_for('settingsPage'))
        return render_template('register.html')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        loginMessage = User.login(email, password)
        flash(loginMessage)
        if loginMessage == 'Login success.':
            return redirect(url_for('settingsPage'))
        return redirect(url_for('loginPage'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')

@app.route('/tutorials/ClashVerge')
def tutorials_ClashVerge():
    return render_template('ClashVerge.html')

@app.route('/toturials/V2rayNG')
def toturials_V2rayNG():
    return render_template('V2rayNG.html')