from server import diceroll

def test_oneDsix():
    roll = diceroll.oneDsix()
    assert roll in range(1, 7)

def test_twoDsix():
    roll = diceroll.twoDsix()
    assert roll in range (2, 13)