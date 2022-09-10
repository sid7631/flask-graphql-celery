from app import create_app
from app.database.init_db import init_db


def main():
    app = create_app()
    with app.app_context():
        init_db()
    return app


if __name__ == '__main__':
    main()
