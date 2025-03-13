from flask import session
from server import diceroll

class Player:
    name: str
    skill: int
    health: int
    luck: int
    potions: int
    gold: int

    initSkill: int #need initial health as potions restore up to original

    def setPlayer(self):
        #session['player_name'] = self.name
        session['player_skill'] = self.skill
        session['player_health'] = self.health
        session['player_init_health'] = self.health
        session['player_luck'] = self.luck
        session['player_potions'] = self.potions
        session['player_gold'] = self.gold
    
    def setName(self, name):
        self.name = name
        session['player_name'] = self.name
    
    def setPotions(self, potions):
        self.potions = potions
        session['player_potions'] = self.potions
    
    def setHealth(self, health):
        self.health = health
        session['player_health'] = self.health
    
    def setSkill(self, skill):
        self.skill = skill
        session['player_skill'] = self.skill

    def setLuck(self, luck):
        self.luck = luck
        session['player_luck'] = self.luck
    
    def setGold(self, gold):
        self.gold = gold
        session['player_gold'] = self.gold

    def getPlayer(self):
        self.name = session['player_name']
        self.skill = session['player_skill']
        self.health = session['player_health']
        self.initHealth = session['player_init_health']
        self.luck = session['player_luck']
        self.potions = session['player_potions']
        self.gold = session['player_gold']

    def clearPlayer(self):
        session.pop('player_name', default=None)
        session.pop('player_skill', default=None)
        session.pop('player_health', default=None)
        session.pop('player_init_health', default=None)
        session.pop('player_luck', default=None)
        session.pop('player_potions', default=None)
        session.pop('player_gold', default=None)

    def rollChar(self):
        self.rollStats()
        self.setPlayer()

    def rollStats(self):
        skillRoll = diceroll.oneDsix() + 6
        self.skill = skillRoll
        healthRoll = diceroll.twoDsix() + 12
        self.health = healthRoll
        self.inithealth = healthRoll
        luckRoll = diceroll.oneDsix() + 6
        self.luck = luckRoll
        self.potions = 1
        self.gold = 0

    def luckTest(self):
        roll = diceroll.twoDsix()
        if self.luck >= roll:
            return [True, roll]
        else: 
            return [False, roll]
        
    def skillTest(self):
        roll = diceroll.twoDsix()
        if self.skill >= roll:
            return [True, roll]
        else: 
            return [False, roll]