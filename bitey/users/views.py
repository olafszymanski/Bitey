from bitey import db, bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from .forms import SignUpForm, LogInForm
from .models import User
from .decorators import is_anonymous


users = Blueprint('users', __name__)


@users.route('/signup', methods=('GET', 'POST'))
@is_anonymous('main.home')
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(form.name.data, form.last_name.data, form.username.data, form.email.data, password)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'info')

        # TODO: Send activation e-mail

        return redirect(url_for('users.login'))

    return render_template('users/signup.html', title='Sign up', form=form)


@users.route('/login', methods=('GET', 'POST'))
@is_anonymous('main.home')
def login():
    form = LogInForm()

    if form.validate_on_submit():
        def validate_and_login(user_object):
            if bcrypt.check_password_hash(user_object.password, form.password.data):
                login_user(user_object)

                return True
            else:
                flash('The password is incorrect!', 'danger')

                return False

        if user := User.query.filter_by(username=form.username_or_email.data).first():
            if validate_and_login(user):
                return redirect(url_for('main.home'))
        elif user := User.query.filter_by(email=form.username_or_email.data).first():
            if validate_and_login(user):
                return redirect(url_for('main.home'))
        else:
            flash('User not found! Please try different credentials.', 'danger')

    return render_template('users/login.html', title='Log in', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('main.home'))
