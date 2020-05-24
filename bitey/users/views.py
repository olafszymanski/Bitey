from bitey import db, bcrypt
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from .forms import SignUpForm, LogInForm, EditUserForm, ChangePasswordForm, ResetPasswordForm
from .models import User
from .decorators import is_anonymous, is_activated, is_not_activated
from .utils import validate_token, send_activation_email, send_password_change_request_email


users = Blueprint('users', __name__)


@users.route('/signup', methods=('GET', 'POST'))
@is_anonymous('main.home')
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(form.username.data, form.email.data, password, form.full_name.data if form.full_name.data.strip() else None,
                    form.address.data if form.address.data.strip() else None)


        if send_activation_email(user, 'Activate Your Account', 'Thank you for signing up. Please follow link below to '
                                                                'activate your account:'):
            flash('We have sent you an e-mail! Check your inbox to activate your account!', 'info')
        else:
            flash('Could not send an activation e-mail!', 'danger')

        db.session.add(user)
        db.session.commit()

        login_user(user)

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
                flash('The password you entered is incorrect!', 'danger')

                return False

        if user := User.query.filter_by(username=form.username_or_email.data).first():
            if validate_and_login(user):
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif user := User.query.filter_by(email=form.username_or_email.data).first():
            if validate_and_login(user):
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('User not found! Please try different credentials.', 'danger')

    return render_template('users/login.html', title='Log in', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('main.home'))


@users.route('/password/reset', methods=('GET', 'POST'))
@is_anonymous('main.home')
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        if send_password_change_request_email(User.query.filter_by(email=form.email.data).first()):
            flash('We have sent you an e-mail! Check your inbox to reset your password!', 'info')

            return redirect(url_for('users.login'))
        else:
            flash('Could not send a reset password e-mail!', 'danger')

    return render_template('users/password-reset.html', title='Reset Password', form=form)


@users.route('/activation/<token>')
def activation(token):
    if email := validate_token(token):
        if user := User.query.filter_by(email=email).first():
            if user.activated:
                flash('Your account is already activated.', 'info')
            else:
                user.activated = True
                user.activated_on = datetime.now()

                db.session.commit()

                flash('Your account has been activated! Thank you!', 'success')
        else:
            flash('User not found!', 'danger')
    else:
        flash('Token is invalid or has expired!', 'danger')

    return redirect(url_for('main.home'))


@users.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', title='Profile')


@users.route('/profile/edit', methods=('GET', 'POST'))
@login_required
@is_activated('users.profile')
def edit():
    form = EditUserForm()

    if request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.address.data = current_user.address
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        current_user.full_name = form.full_name.data if form.full_name.data.strip() else None
        current_user.address = form.address.data if form.address.data.strip() else None
        current_user.username = form.username.data
        if form.email.data != current_user.email:
            current_user.email = form.email.data
            current_user.activated = False

            db.session.commit()

            if send_activation_email(current_user, 'Activate Your Account', "We've noticed that you have changed your "
                                                                            "e-mail, you will now how to reactivate your "
                                                                            "account. Please follow link below to "
                                                                            "activate your account:"):
                flash('We have sent you an e-mail! Check your inbox to reactivate your account!', 'info')
            else:
                flash('Could not send an activation e-mail!', 'danger')

        else:
            db.session.commit()

            flash('Your profile has been edited successfully!', 'success')

        return redirect(url_for('users.profile'))

    return render_template('users/edit.html', title='Edit', form=form)


@users.route('/profile/password/change/request')
@login_required
@is_activated('users.profile')
def password_change_request():
    if send_password_change_request_email(current_user):
        flash('We have sent you an e-mail! Check your inbox to change your password!', 'info')
    else:
        flash('Could not request password change!', 'danger')

    return redirect(url_for('users.profile'))


@users.route('/profile/password/change/<token>', methods=('GET', 'POST'))
def password_change(token):
    if email := validate_token(token):
        if user := User.query.filter_by(email=email).first():
            form = ChangePasswordForm()

            if form.validate_on_submit():
                user.password = bcrypt.generate_password_hash(form.password.data)

                db.session.commit()

                flash('Your password has been changed!', 'success')

                return redirect(url_for('users.profile'))

            return render_template('users/password-change.html', title='Change Password', form=form)
        else:
            flash('User not found!', 'danger')
    else:
        flash('Token is invalid or has expired!', 'danger')

    return redirect(url_for('users.profile'))


@users.route('/profile/resend')
@login_required
@is_not_activated('users.profile')
def resend():
    # TODO: Add cooldown (?)
    if send_activation_email(current_user, 'Activate Your Account', "We've noticed that you have changed your e-mail, "
                                                                    "you will now how to reactivate your account. Please "
                                                                    "follow link below to activate your account:"):
        flash('We have sent you an e-mail! Check your inbox to activate your account!', 'info')
    else:
        flash('Could not send an activation e-mail!', 'danger')

    return redirect(url_for('users.profile'))
