from pcaw_site import app
from flask import render_template, redirect, url_for, session, request
from users.form import RegisterForm, LoginForm
from pcaw_site import db
from users.models import User
from users.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
    
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data,
            ).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                session['username'] = form.username.data
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = "Incorrect password"
        else:
            error = "User not found"
    return render_template('users/login.html', form=form, error=error)
        
    
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        db.create_all()
        user = User(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('users/register.html', form=form)
    
@app.route('/success')
def success():
    return "User Register"

@app.route('/vip')
@login_required
def vip():
    return render_template('vip/vip.html')
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))