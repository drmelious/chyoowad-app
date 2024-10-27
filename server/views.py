from flask import Blueprint, render_template, request
from server import entity, diceroll
import json

views = Blueprint('views', __name__)
myCharacter = entity.Player()
currentMonster = entity.Monster()
currentPage = 0
inCombat = False

def openBook():
    with open('server/books/first_steps.json') as data:
        book = json.load(data)
        return book

@views.route('/', methods=["GET", "POST"])
def home():
    global currentPage
    currentPage = 0
    myCharacter.resetChar()
    return render_template('char_name.html')

@views.route('/stats', methods=["POST"])
def stats():
    myCharacter.resetChar()
    name = request.form.get("name")
    #in case they rerolled
    if name is not None: 
        myCharacter.name = name
    return render_template('char_stats.html', character=myCharacter)

@views.route('/potion', methods=["POST"])
def potion():
    if myCharacter.potions > 0:
        noPotions = False
        myCharacter.potions -= 1
        myCharacter.health = myCharacter.inithealth
    else:
        noPotions = True
    return render_template("used_potion.html", character=myCharacter, noPotions=noPotions)

#used for index page in book
@views.route('/intro', methods=["POST"])
def intro():
    book = openBook()
    page=book["pages"][0]
    return render_template("intro.html", page=page, character=myCharacter) 

#used for all other pages in book
@views.route('/page', methods=["POST"])
def page():
    #if already in combat go back there (potion)
    global inCombat
    if inCombat:
        return render_template("combat_start.html", character=myCharacter, monster=currentMonster)
    else:
        #open book and get the last choice made
        book = openBook()
        global currentPage
        #got back to original page if coming from potion
        if request.form['choice'] == "potion":
            page=book["pages"][currentPage]
        else:
            choice = int(request.form['choice'])
            #find the next page based on the choice made
            nextPage = book["pages"][currentPage]["options"][choice]["next_page"]
            page=book["pages"][nextPage]
            currentPage = nextPage
        #choose which template to use based on page type
        if page["type"] == "one_choice":
            return render_template("one_choice.html", page=page, character=myCharacter)
        elif page["type"] == "two_choices":
            return render_template("two_choices.html", page=page, character=myCharacter)
        elif page["type"] == "combat_start":
            monsterName = page["monster"]["name"]
            monsterSkill = page["monster"]["skill"]
            monsterHealth = page["monster"]["health"]
            inCombat = True
            currentMonster.setMonster(monsterName, monsterSkill, monsterHealth)
            return render_template("combat_start.html", character=myCharacter, monster=currentMonster)
        elif page["type"] == "test":
            if page["stat"] == "skill":
                result = myCharacter.skillTest()
            elif page["stat"] == "luck":
                result = myCharacter.luckTest()
            return render_template("test.html", page=page, character=myCharacter, passed=result)
        elif page["type"] == "stat_change":
            stat = page["stat"]
            change = page["change"]
            amount = page["amount"]
            if change == "+":
                #I'm sure there is a better way to do this using stat directly
                if stat == "health":
                    myCharacter.health += amount
                elif stat == "skill":
                    myCharacter.skill += amount
                elif stat == "luck":
                    myCharacter.luck += amount
                elif stat == "gold":
                    myCharacter.gold += amount
            elif change == "-":
                if stat == "health":
                    myCharacter.health -= amount
                elif stat == "skill":
                    myCharacter.skill -= amount
                    if myCharacter.skill < 0:
                        myCharacter.skill = 0
                elif stat == "luck":
                    myCharacter.luck -= amount
                    if myCharacter.luck < 0:
                        myCharacter.luck = 0
                    #I don't intend taking gold off the character - treating it like a score
            if myCharacter.health <= 0:
                return render_template("you_died.html")
            else:
                return render_template("one_choice.html", page=page, character=myCharacter)       
        else:
            currentPage = 0
            return render_template("char_name.html")

@views.route('/combat', methods=["POST"])
def combat():
    global inCombat
    #roll dice and work out who won this round
    playerAttack = diceroll.twoDsix() + myCharacter.skill
    monsterAttack = diceroll.twoDsix() + currentMonster.skill #+ 20 #make the monster win
    if playerAttack >= monsterAttack:
        currentMonster.health -= 2
        playerWin = True
    else:
        myCharacter.health -= 2
        playerWin = False
    #work out if someones dead and direct to appropriate page    
    if myCharacter.health <= 0:
        inCombat = False
        return render_template("you_died.html")
    elif currentMonster.health <= 0:
        inCombat = False
        return render_template("combat_won.html", character=myCharacter, monster=currentMonster)
    else:
        return render_template("combat.html", character=myCharacter, monster=currentMonster, playerWin=playerWin, playerAttack=playerAttack, monsterAttack=monsterAttack)