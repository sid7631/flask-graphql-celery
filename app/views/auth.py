import datetime

from flask import Blueprint, redirect, render_template, flash, jsonify, session
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from app.models.user_models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import os
from app import db
from flask import current_app as app
# from app.models.feedeater_models import Feed
from app.models.user_models import UserProfileForm
from app.utils.create_folder import create_folder
from .forms import LoginForm

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')

@auth_blueprint.route('/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        form = LoginForm(request.form)
        remember = True if request.form.get('remember') else False

        # Verify the sign in form
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                login_user(user, remember=remember)
                flash('Welcome %s' % user.username)
                return redirect("/portfolio")

            flash('Wrong email or password', 'error-message')
        return render_template("auth/signin.html", form=form)

    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/portfolio')
        form = LoginForm(request.form)
        return render_template('auth/signin.html', form=form)


@auth_blueprint.route("/signup/", methods=["POST", "GET"])
@auth_blueprint.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        create_folder(os.path.join(app.config['DATA_FOLDER'],username))

        return redirect(url_for('auth.signin'))
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect('/portfolio')
        return render_template('auth/signup.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged yourself out.')
    return redirect(url_for('auth.signin'))