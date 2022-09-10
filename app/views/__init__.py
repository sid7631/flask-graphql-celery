from .main_view import main_blueprint
from .auth import auth_blueprint


def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)