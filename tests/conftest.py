import pytest

from app import app, create_app, db

@pytest.fixture
def client():
    client = app.test_client()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['WTF_CSRF_ENABLED'] = False

    context = app.app_context()
    context.push()

    db.create_all()

    yield client

    db.session.remove()
    db.drop_all()

    context.pop()