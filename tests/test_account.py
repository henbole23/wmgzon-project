from app.models import Users
from app.extensions import db, bcrypt


def test_registration(client, app):
    """Function for testing registration functionality works"""

    # Get request for the registration page
    response = client.get('/register')
    # Check register page loaded
    assert b'<h3>Register</h3>' in response.data
    # Check load status is success
    assert response.status_code == 200

    # Mock user registration data
    mock_data = {'email': 'test@test.com', 'username': 'test1',
                 'password': 'password123', 'confirm': 'password123'}

    # Post request for registering the user
    response = client.post('/register', data=mock_data, follow_redirects=True)
    # Check load status is success
    assert response.status_code == 200
    with app.app_context():
        user = db.session.query(Users).first()
        # Checks a row has been added to the database
        assert db.session.query(Users).count() == 1
        # Checks the correct email has been added
        assert user.email == mock_data['email']  # type: ignore
        # Checks that the password stored isn't what the user entered (has been hashed)
        assert user.password != mock_data['password']  # type: ignore


def test_customer_login(client, app):
    """Function for testing login functionality works"""

    with client:
        # Get request for the login page
        response = client.get('/login')
        # Check login page loaded
        assert b'<h3>Login</h3>' in response.data
        # Check load status is success
        assert response.status_code == 200

        mock_data = {'email': 'test@test.com', 'username': 'test1',
                     'password': 'password123', 'confirm': 'password123'}

        mock_customer = Users(email=mock_data['email'],
                              username=mock_data['username'],
                              password=bcrypt.generate_password_hash(mock_data['password']))
        with app.app_context():
            # Adds mock_user to the database
            db.session.add(mock_customer)
            db.session.commit()

        # Post request for customer login
        response = client.post('/login', data=mock_data, follow_redirects=True)

        # Check load status is success after the post request
        assert response.status_code == 200
