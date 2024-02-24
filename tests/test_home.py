# Tests to see if page loaded
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
