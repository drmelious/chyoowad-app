from server import diceroll

#character = {"skill":10, "stamina":19, "luck":10}
class Player:
    def __init__(self):
        self.resetChar()

    def resetChar(self):
        self.skill = 10
        self.initSkill = 10
        self.stamina = 19
        self.initStamina = 19
        self.luck = 10
        self.initLuck = 10
        self.provisions = 10
        self.gold = 0
        self.items = ["Sword", "Leather Armour"]
        self.dragonFire = False

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
    def setMonster(self, name, skill, stamina):
        self.name = name
        self.skill = skill
        self.stamina = stamina