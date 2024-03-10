from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'raedmad3ouk'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mock user database


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


# Replace this with a real user database
users = {'1': User('1'), '2': User('2')}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = users.get(user_id)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('create_account.html')  # Render the combined page


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.id}! This is your dashboard.'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/create_account')
def create_account():
    return render_template('create_account.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences.html')


@app.route('/generated_recipe')
def generated_recipe():
    return render_template('generated_recipe.html')


if __name__ == '__main__':
    app.run(debug=True)


