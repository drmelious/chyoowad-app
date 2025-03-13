from flask import session

def set_base_session_data(test_client):
    with test_client.session_transaction() as session:
        session['in_combat'] = False 
        
        session['player_name'] = 'asas'
        session['player_skill'] = 12
        session['player_health'] = 10
        session['player_init_health'] = 100
        session['player_luck'] = 12
        session['player_potions'] = 1
        session['player_gold'] = 0

#GIVEN the player has tried to use a potion
#WHEN their health is lower than their intial health
#THEN they get their health back, lose one potion and get the right response
def test_used_potion(test_client):
    set_base_session_data(test_client)
    response = test_client.post('/potion')
    assert session['player_health'] == session['player_init_health']
    assert session['player_potions'] == 0 
    assert b"You used" in response.data

#GIVEN the player has tried to use a potion
#WHEN the player is already at their max health
#THEN they do not lose a potion, stay at the same health and get the right response
def test_max_health(test_client):
    set_base_session_data(test_client)
    with test_client.session_transaction() as session:
        session['player_health'] = 100
    response = test_client.post('/potion')
    assert session['player_potions'] == 1
    assert session['player_health'] == 100
    assert b"You are already" in response.data

#GIVEN the player has tried to use a potion
#WHEN the player does not have any potions
#THEN they still don't have any potions, stay at the same health get the right response
def test_no_potions(test_client):
    set_base_session_data(test_client) 
    with test_client.session_transaction() as session:
        session['player_potions'] = 0
    response = test_client.post('/potion')
    assert session['player_potions'] == 0
    assert session['player_health'] == 10
    assert b"You don't" in response.data