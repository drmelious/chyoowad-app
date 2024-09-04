from flask import Blueprint, render_template, request
from server import entity, diceroll

views = Blueprint('views', __name__)
myCharacter = entity.Player()
currentMonster = entity.Monster()
returnPage = 0
escapePage = 0

@views.route('/', methods=["GET", "POST"])
def home():
    myCharacter.resetChar()
    return render_template("char_creation.html")

@views.route('/intro', methods=["POST"])
def intro():
    #get character input
    name = request.form.get("name")
    myCharacter.name = name
    myCharacter.potionCount = 2
    if request.form["potionChoice"] == "skillPotion":
        myCharacter.potionType = "skill"
    elif request.form["potionChoice"] == "staminaPotion":
        myCharacter.potionType = "stamina"
    elif request.form["potionChoice"] == "luckPotion":
        myCharacter.potionType = "luck"
    else:
        myCharacter.potionType = "none"
        myCharacter.potionCount = 0
    myCharacter.potionDisplay = myCharacter.potionType.title()
    return render_template("intro.html", character=myCharacter)

@views.route('/usedPotion', methods=["POST"])
def usedPotion():
    if myCharacter.potionCount > 0:
        noPotions = False
        myCharacter.potionCount -= 1
        if myCharacter.potionType == "skill":
            myCharacter.skill = myCharacter.initSkill
        elif myCharacter.potionType == "stamina":
            myCharacter.stamina = myCharacter.initStamina
        elif myCharacter.potionType == "luck":
            myCharacter.luck = myCharacter.initLuck
    else:
        noPotions = True
    return render_template("used_potion.html", character=myCharacter, monster=currentMonster, noPotions=noPotions)

@views.route('/usedProvision', methods=["POST"])
def usedProvision():
    if myCharacter.provisions == 0:
        noProvisions = True
    else: 
        myCharacter.provisions -= 1
        myCharacter.stamina += 4
        if myCharacter.stamina > myCharacter.initStamina:
            myCharacter.stamina = 19
        noProvisions = False
    return render_template("used_provision.html", character=myCharacter, noProvisions=noProvisions)

@views.route('/combatStart', methods=["POST"])
def combatStart():
    return render_template("combat_start.html", character=myCharacter, monster=currentMonster, escape=escapePage)

@views.route('/combat', methods=["POST"])
def combat():
    #roll dice and work out who won this round
    playerAttack = diceroll.twoDsix() + myCharacter.skill
    monsterAttack = diceroll.twoDsix() + currentMonster.skill #+ 20 make the monster win
    if playerAttack >= monsterAttack:
        currentMonster.stamina -= 2
        playerWin = True
    else:
        myCharacter.stamina -= 2
        playerWin = False
    #work out if someones dead and direct to appropriate page    
    if myCharacter.stamina <= 0:
        myCharacter.resetChar()
        return render_template("you_died.html")
    elif currentMonster.stamina <= 0:
        pageString = "pages/page"+str(returnPage)+"r.html"
        return render_template(pageString, character=myCharacter, playerAttack=playerAttack, monsterAttack=monsterAttack)
    else:
        return render_template("combat.html", character=myCharacter, monster=currentMonster, playerWin=playerWin, playerAttack=playerAttack, monsterAttack=monsterAttack, escape=escapePage)

@views.route('/escape', methods=["POST"])
def escape():
    global escapePage
    pageString = "pages/page"+str(escapePage)+".html"
    escapePage = 0
    return render_template(pageString, character=myCharacter)

@views.route('/return', methods=["POST"])
def goBack():
    global returnPage
    pageString = "pages/page"+str(returnPage)+".html"
    return render_template(pageString, character=myCharacter)
