from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from server import app, db
from server.models import User, GiftCard, Service, addUserToDB

import re

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('settings'))
        
        form_type = request.form.get('form_type')

        if form_type == 'password':
            password = request.form['password']
            if not password:
                flash('Empty password.')
                return redirect(url_for('settings'))
            current_user.setPassword(password)
            db.session.commit()
            flash('Password updated.')
            return redirect(url_for('settings'))
        elif form_type == 'recharge':
            amount = request.form['amount']

            # input checking
            if not amount:
                flash('Empty amount.')
                return redirect(url_for('settings'))
            
            if len(amount) < 10 and amount.isdigit():
                amount = int(amount)
            else:
                flash('Amount invalid')
                return redirect(url_for('settings'))
            
            current_user.rechargeBalance(amount)
            db.session.commit()
            flash('Balance updated.')
            return redirect(url_for('settings'))

    balance = current_user.getBalance()
    return render_template('settings.html', balance=balance)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        refer = request.form['refer']

        if not email:
            flash('Empty email.')
            return redirect(url_for('register'))
        
        if not password:
            flash('Empty password.')
            return redirect(url_for('register'))

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if len(email) > 128 or not re.match(pattern, email):
            flash('Invalid email.')
            return redirect(url_for('register'))

        repeated = User.query.filter_by(email=email).all()
        if repeated:
            flash('Repeated email.')
            return redirect(url_for('register'))
            
        if refer:
            addUserToDB(email, password, 2, referee=refer)
        else:
            addUserToDB(email, password, 2)

        flash('Register succcess.')
        return redirect(url_for('settings'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email:
            flash('Empty email.')
            return redirect(url_for('login'))
        
        if not password:
            flash('Empty password.')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email not registered.')
            return redirect(url_for('login'))
        
        if email == user.email and user.validatePassword(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

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