from flask import session

def set_base_session_data(test_client):
    with test_client.session_transaction() as session:
        session['in_combat'] = False   
        session['player_name'] = 'asas'
        session['player_skill'] = 12
        session['player_health'] = 100
        session['player_init_health'] = 100
        session['player_luck'] = 12
        session['player_potions'] = 1
        session['player_gold'] = 0

def call_page(test_client, current_page, choice):
    with test_client.session_transaction() as session:
        session['current_page'] = current_page
    return test_client.post('/page', data={"choice": choice})      

def test_intro(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 0, 'intro')
    assert b'Introduction' in response.data

def test_one_choice_page(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 0, 0)    
    assert response.text.count("<button") == 3

def test_two_choice_page(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 1, 0)
    assert response.text.count("<button") == 4

def test_combat_start(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 2, 0)
    assert b"Monster:" in response.data

def test_test_page(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 3, 0)
    assert b"You rolled" in response.data

def test_stat_change(test_client):
    set_base_session_data(test_client)
    call_page(test_client, 4, 1)
    assert session['player_health'] == 98

def test_broken_page(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 5, 0)
    assert b"Unrecognised" in response.data

def test_end(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 6, 0)
    assert b"Looks like" in response.data

def test_potion_return(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 1, 'potion')
    assert response.text.count("<button") == 3

def test_potion_intro_return(test_client):
    set_base_session_data(test_client)
    response = call_page(test_client, 0, 'potion')
    assert b'Introduction' in response.data