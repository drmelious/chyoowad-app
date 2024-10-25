from server import diceroll

#character = {"skill":10, "stamina":19, "luck":10}
class Player:
    def __init__(self):
        self.resetChar()

    def resetChar(self):
        skillRoll = diceroll.oneDsix() + 6
        self.skill = skillRoll
        self.initSkill = skillRoll
        healthRoll = diceroll.twoDsix() + 12
        self.health = healthRoll
        self.inithealth = healthRoll
        luckRoll = diceroll.oneDsix() + 6
        self.luck = luckRoll
        self.initluck = luckRoll
        self.potions = 1
        self.gold = 0

    def luckTest(self):
        roll = diceroll.twoDsix()
        #test failing
        #roll = 20
        if self.luck >= roll:
            return [True, roll]
        else: 
            return [False, roll]
        
    def skillTest(self):
        roll = diceroll.twoDsix()
        #test failing
        #roll = 20
        if self.skill >= roll:
            return [True, roll]
        else: 
            return [False, roll]

class Monster:
    def setMonster(self, name, skill, health):
        self.name = name
        self.skill = skill
        self.health = health