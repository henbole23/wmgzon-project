from app.models import Users

def test_registration(client, app):
    response = client.get('/register')
    assert b'<h3>Register</h3>' in response.data
    assert response.status_code == 200
    
    response = client.post('/register', data={'email': 'test@test.com', 'username':'test1', 'password': 'password123', 'confirm':'password123'}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Users.query.count() == 1
        assert Users.query.first.email == 'test@test.com'