from flask import Blueprint, render_template, request, session
from server import diceroll
from server.monster import Monster
from server.player import Player
import json

views = Blueprint('views', __name__)

#FUNCTIONS
def openBook():
    with open('server/books/first_steps.json') as data:
        book = json.load(data)
    return book

def loadNextPage(book, choice):
    currentPage = session['current_page']
    nextPage = book["pages"][currentPage]["options"][choice]["next_page"]
    page = book["pages"][nextPage]
    session['current_page'] = nextPage
    return page

def newMonster(page):
    monster = Monster()
    monster.setMonster(page["monster"]["name"], page["monster"]["skill"], page["monster"]["health"])
    #return monster

#ROUTES
@views.route('/', methods=["GET", "POST"])
def home():
    #reset everything for returning to this page via home
    session['current_page'] = 0
    session['in_combat'] = False
    player = Player()
    player.clearPlayer()
    monster = Monster()
    monster.clearMonster()
    return render_template('char_name.html')

@views.route('/stats', methods=["POST"])
def stats():
    player = Player()
    player.rollChar()
    name = request.form.get("name")
    if name is not None:     #in case they rerolled so don't overwrite name with blank
        player.setName(name)
    player.getPlayer() #only really need to get the name for rerolling but just getting whole thing again
    return render_template('char_stats.html', character=player)

#used for index page in book
@views.route('/intro', methods=["POST"])
def intro():
    book = openBook()
    player = Player()
    player.getPlayer()

    try:
        page=book["pages"][0]
        return render_template("intro.html", page=page, character=player)
    except KeyError:
        errText = "Cannot find a pages attribute in the book."
        return render_template("json_error.html", text=errText)
    except IndexError:
        errText = "There are not any pages in the book."
        return render_template("json_error.html", text=errText)

#used for all other pages in book
@views.route('/page', methods=["POST"])
def page():
    player = Player()
    player.getPlayer()
    inCombat = session['in_combat']
    if inCombat:     #if already in combat go back there (potion)
        monster = Monster()
        monster.getMonster()
        return render_template("combat_start.html", character=player, monster=monster)
    else:
        book = openBook()
        currentPage = session['current_page']
        #go back to original page if coming from potion
        if request.form['choice'] == "potion":
            page=book["pages"][currentPage]
        else:
            #get choice from page they came from and find the page to go to
            choice = int(request.form['choice'])
            page = loadNextPage(book, choice)
        #choose which template to use based on page type
        if page["type"] == "one_choice":
            return render_template("one_choice.html", page=page, character=player)
        elif page["type"] == "two_choices":
            return render_template("two_choices.html", page=page, character=player)
        elif page["type"] == "combat_start":
            newMonster(page)
            monster = Monster()
            monster.getMonster()
            session['in_combat'] = True
            return render_template("combat_start.html", character=player, monster=monster)
        elif page["type"] == "test":
            if page["stat"] == "skill":
                result = player.skillTest()
            elif page["stat"] == "luck":
                result = player.luckTest()
            return render_template("test.html", page=page, character=player, passed=result)
        elif page["type"] == "stat_change":
            stat = page["stat"]
            change = page["change"]
            amount = page["amount"]
            if change == "+":
                #I'm sure there is a better way to do this using stat directly
                if stat == "health":
                    health = player.health + amount
                    player.setHealth(health)
                elif stat == "skill":
                    skill = player.skill + amount
                    player.setSkill(skill)
                elif stat == "luck":
                    luck = player.luck + amount
                    player.setLuck(luck)
                elif stat == "gold":
                    gold = player.gold + amount
                    player.setGold(gold)
            elif change == "-":
                if stat == "health":
                    health = player.health - amount
                    player.setHealth(health)
                elif stat == "skill":
                    skill = player.skill - amount
                    if skill < 0:
                        skill = 0
                    player.setSkill(skill)
                elif stat == "luck":
                    luck = player.luck - amount
                    if luck < 0:
                        luck = 0
                    player.setLuck(luck)
                    #I don't intend taking gold off the character - treating it like a score
            if player.health <= 0:
                return render_template("you_died.html")
            else:
                return render_template("one_choice.html", page=page, character=player)       
        elif page["type"] == "end":
            session['current_page'] = 0
            player = Player()
            player.clearPlayer()
            return render_template("char_name.html")
        else:
            errText = "Unrecognised page type"
            return render_template("json_error.html", text=errText)

@views.route('/combat', methods=["POST"])
def combat():
    player = Player()
    player.getPlayer()
    monster = Monster()
    monster.getMonster()

    #roll dice and work out who won this round
    playerAttack = diceroll.twoDsix() + player.skill
    monsterAttack = diceroll.twoDsix() + monster.skill #+ 20 #make the monster win

    if playerAttack >= monsterAttack:
        monsterHealth = monster.health - 2
        monster.setHealth(monsterHealth)
        playerWin = True
    else:
        playerHealth = player.health - 2
        player.setHealth(playerHealth)
        playerWin = False

    #work out if someones dead and direct to appropriate page    
    if player.health <= 0:
        session['in_combat'] = False
        return render_template("you_died.html")
    elif monster.health <= 0:
        
        session['in_combat'] = False
        monster.clearMonster()
        return render_template("combat_won.html", character=player, monster=monster)
    else:
        return render_template("combat.html", character=player, monster=monster, playerWin=playerWin, playerAttack=playerAttack, monsterAttack=monsterAttack)
    
@views.route('/potion', methods=["POST"])
def potion():
    player = Player()
    player.getPlayer()

    if player.potions > 0:
        noPotions = False
        potions = player.potions - 1
        player.setPotions(potions)
        player.setHealth(player.initHealth)
    else:
        noPotions = True
    return render_template("used_potion.html", character=player, noPotions=noPotions)