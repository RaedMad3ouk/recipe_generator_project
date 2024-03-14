from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'raedmad3ouk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'error')
    return render_template('create_account.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! This is your dashboard.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

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

    return render_template('generated_recipe.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
