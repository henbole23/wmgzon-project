import pytest
from app import create_app, db


@pytest.fixture()
# Configuration of the app test environment
def app():
    # Creates database in memory which saves teardown of database after each test
    app = create_app(database="sqlite://")
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
# Configuration of the mock client
def client(app):
    return app.test_client()
