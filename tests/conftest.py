import os
import pytest
from dotenv import load_dotenv

from app import create_app
from db import db
from sqlalchemy import delete
from models.user import UserModel


@pytest.fixture(scope="function")
def app():
    load_dotenv()
    app = create_app(os.getenv("TEST_DATABASE_URL"))
    app.config.update({"TESTING": True})

    yield app

    # cleanup
    with app.app_context():
        clear_users = delete(UserModel)
        db.session.execute(clear_users)
        db.session.commit()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
