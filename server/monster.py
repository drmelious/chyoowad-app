from flask import session

class Monster:
    name: str
    skill: int
    health: int

    def setMonster(self, name, skill, health):
        session['monster_name'] = name
        session['monster_skill'] = skill
        session['monster_health'] = health

    def getMonster(self):
        self.name = session['monster_name']
        self.skill = session['monster_skill']
        self.health = session['monster_health']

    def clearMonster(self):
        session.pop('monster_name', default=None)
        session.pop('monster_skill', default=None)
        session.pop('monster_health', default=None)
    
    def setHealth(self, health):
        self.health = health
        session['monster_health'] = self.health