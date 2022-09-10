# This file defines command line commands for manage.py

import datetime

from flask import current_app
from werkzeug.security import generate_password_hash

from app.models.user_models import User, Role
from app.database import db


def init_db():
    """ Initialize the database."""

    # Uncomment from below
    # db.drop_all()
    # db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role( 'admin', u'Admin')
    member_role = find_or_create_role('member', u'Member')

    # Add users
    user = find_or_create_user(u'Admin', u'Admin@gmail.com', u'Example',  u'A', 'Password1', admin_role)
    user = find_or_create_user(u'Member',  u'Member@gmail.com', u'Example', u'M', 'Password1', member_role)

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(username, email, first_name,last_name, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name= last_name,
                    password=generate_password_hash(password, method='sha256'),
                    active=True)
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user


