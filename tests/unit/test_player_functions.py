from server.player import Player

def test_unlucky_player():
    player = Player()
    player.luck = 0
    result = player.luckTest()
    assert result[0] == False
    assert result[1] in range(2, 13)

def test_lucky_player():
    player = Player()
    player.luck = 12
    result = player.luckTest()
    assert result[0] == True
    assert result[1] in range(2, 13)

def test_unskillful_player():
    player = Player()
    player.skill = 0
    result = player.skillTest()
    assert result[0] == False
    assert result[1] in range(2, 13)

def test_skillful_player():
    player = Player()
    player.skill = 12
    result = player.skillTest()
    assert result[0] == True
    assert result[1] in range(2, 13)

def test_roll_stats():
    player = Player()
    player.rollStats()
    assert player.skill in range(7, 13)
    assert player.health in range(14, 25)
    assert player.luck in range(7, 13)
    assert player.potions == 1
    assert player.gold == 0