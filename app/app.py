from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import User, Game, Case
from forms import RegistrationForm, LoginForm
from config import Config




app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db = SQLAlchemy(app)  
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
import os
print(os.listdir('templates'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/game')
@login_required
def game():
    
    selected_case = 1
    cases = [
        {'id': i, 'is_open': False}
        for i in range(1, 27)
    ]
    return render_template('game.html', selected_case=selected_case, cases=cases)

@app.route('/open_case/<int:case_id>', methods=['GET'])
@login_required
def open_case(case_id):
    amount = 1000  
    return jsonify(amount=amount)

@app.route('/deal', methods=['POST'])
@login_required
def deal():
    offer_amount = 50000  
    return jsonify(amount=offer_amount)

@app.route('/no_deal', methods=['POST'])
@login_required
def no_deal():
    return jsonify(success=True)

@app.route('/keep_case', methods=['POST'])
@login_required
def keep_case():
    amount = 100000 
    return jsonify(amount=amount)

@app.route('/switch_case', methods=['POST'])
@login_required
def switch_case():
    amount = 75000  
    return jsonify(amount=amount)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
