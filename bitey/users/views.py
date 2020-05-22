from flask import Blueprint, render_template
from .forms import SignUpForm, LogInForm


users = Blueprint('users', __name__)


@users.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()

    return render_template('users/signup.html', title='Sign up', form=form)


@users.route('/login', methods=('GET', 'POST'))
def login():
    form = LogInForm()

    return render_template('users/login.html', title='Log in', form=form)
