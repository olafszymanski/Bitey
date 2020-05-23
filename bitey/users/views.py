from bitey import db, bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from datetime import datetime
from .forms import SignUpForm, LogInForm
from .models import User
from .decorators import is_anonymous
from .utils import generate_confirmation_token, confirm_token, send_email


users = Blueprint('users', __name__)


@users.route('/signup', methods=('GET', 'POST'))
@is_anonymous('main.home')
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(form.name.data, form.last_name.data, form.username.data, form.email.data, password)

        token = generate_confirmation_token(user)
        url = url_for('users.activation', token=token, _external=True)
        content = render_template('users/emails/account_activation.html', name=(user.name if user.name else user.username), url=url)
        send_email('Activate Your Account', user.email, content)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('We have sent you a confirmation e-mail, check your inbox and activate your account!', 'info')

        return redirect(url_for('main.home'))

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


@users.route('/activation/<token>')
def activation(token):
    try:
        email = confirm_token(token)
    except:
        flash('Token is invalid or has expired!', 'danger')

    user = User.query.filter_by(email=email).first()
    if user.activated:
        flash('Your account is already activated.', 'info')
    else:
        user.activated = True
        user.activated_on = datetime.now()

        db.session.commit()

        flash('Your account has been activated! Thank you!', 'success')

    return redirect(url_for('main.home'))
