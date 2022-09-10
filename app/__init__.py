from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_user import UserManager
from flask_graphql import GraphQL, GraphQLView
from flask_login import LoginManager

# Instantiate Flask extensions
from app import celeryapp
from app.database import db
from app.schema.schema import schema

csrf_protect = CSRFProtect()

migrate = Migrate()


def create_app(extra_config_settings={}):
    """
    Create a Flask Application
    :return:
    """
    app = Flask(__name__)

    # Load common config
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings
    app.config.update(extra_config_settings)

    # register blueprint here
    from .views import register_blueprints
    register_blueprints(app)

    # Setup Flask-SQLAlchemy
    db.init_app(app)
    db.app = app
    # db.create_all()
    from app.commands.init_db import create_users
    # create_users(db)

    # Set up Flask Migrate
    migrate.init_app(app, db)

    # Set up WTForms CSRProtect
    # csrf_protect.init_app(app)

    # Celery
    celery = celeryapp.create_celery_app(app)
    celeryapp.celery = celery

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    # from wtforms.fields import HiddenField
    #
    # def is_hidden_field_filter(field):
    #     return isinstance(field, HiddenField)

    # app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    from app.models.user_models import User

    # Set up Flask-User
    # user_manager = UserManager(app, db, User)

    # @app.context_processor
    # def context_processor():
    #     return dict(user_manager=user_manager)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    @app.route('/ok')
    def home():
        return 'home'

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # for having the GraphiQL interface
        )
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
