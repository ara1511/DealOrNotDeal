from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from . import db, bcrypt
from .models import User
from .forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    pass

@main.route("/login", methods=['GET', 'POST'])
def login():
    pass

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
