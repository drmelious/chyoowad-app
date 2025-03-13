from flask import session

def set_base_session_data(test_client):
    with test_client.session_transaction() as session:
        session['monster_name'] = 'Goblin'
        session['monster_skill'] = 12
        session['monster_health'] = 100
        
        session['player_name'] = 'asas'
        session['player_skill'] = 12
        session['player_health'] = 100
        session['player_init_health'] = 100
        session['player_luck'] = 12
        session['player_potions'] = 1
        session['player_gold'] = 0

#GIVEN player and monster are in combat
#WHEN monster is not on low health and loses
#THEN player hits monster and it loses 2 health
def test_player_wins(test_client):
    set_base_session_data(test_client)
    with test_client.session_transaction() as session:
        session['monster_skill'] = 1

    response = test_client.post('/combat')
    
    #with test_client.session_transaction() as session:
    with test_client:
        assert session['monster_health'] == 98
    assert b"You hit" in response.data

#GIVEN player and monster are in combat
#WHEN player is not on low health and loses
#THEN monster hits the player
def test_monster_wins(test_client):
    set_base_session_data(test_client)
    with test_client.session_transaction() as session:
        session['player_skill'] = 1

    response = test_client.post('/combat')
    assert b"hit you" in response.data

#GIVEN player and monster are in combat
#WHEN monster is on low health and loses
#THEN monster dies
def test_monster_dies(test_client):
    set_base_session_data(test_client)
    with test_client.session_transaction() as session:
        session['monster_skill'] = 1
        session['monster_health'] = 2

    response = test_client.post('/combat')
    assert b"You defeated" in response.data

#GIVEN player and monster are in combat
#WHEN player is on low health and loses
#THEN player dies
def test_player_dies(test_client):
    set_base_session_data(test_client)
    with test_client.session_transaction() as session:
        session['player_skill'] = 1
        session['player_health'] = 2
    
    response = test_client.post('/combat')
    assert b"You Died" in response.data