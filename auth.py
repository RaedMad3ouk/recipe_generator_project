from flask import flash, redirect, url_for, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from main import app, db, User


def register_user(email, username, password):
    if len(username) < 4:
        flash('Username must be at least 4 characters long.', 'error')
        return redirect(url_for('create_account'))

    if len(password) < 4:
        flash('Password must be at least 4 characters long.', 'error')
        return redirect(url_for('create_account'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email is already taken. Choose a different one.', 'error')
        return redirect(url_for('create_account'))

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! You can now log in.', 'success')
    return redirect(url_for('login'))


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return True

    flash('Invalid email or password. Please try again.', 'error')
    return False


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        return register_user(email, username, password)
    return render_template('create_account.html')
