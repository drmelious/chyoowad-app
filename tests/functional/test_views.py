from flask import session

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_player_name_set(test_client):
    test_client.post('/stats', data={"name": "asas"})
    assert session['player_name'] == 'asas'
