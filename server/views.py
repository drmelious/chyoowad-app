from flask import Blueprint, render_template, redirect, request, session, url_for
from server import diceroll, utils
from server.monster import Monster
from server.player import Player

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
def home():
    #reset everything for returning to this page via home link
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

#used for all other pages in book
@views.route('/page', methods=["POST"])
def page():
    player = Player()
    player.getPlayer()

    book = utils.openBook()
    currentPage = session['current_page']
    choice = request.form['choice']

    #don't advance the page if coming to the intro or from potion page
    if choice == "intro" or choice == "potion":
        page=book["pages"][currentPage]
    else:
        #get choice from page they came from and find the page to go to
        intChoice = int(choice)
        page = utils.loadNextPage(book, intChoice)

    #choose which template to use based on page type
    if page["type"] == "intro":
        return render_template("intro.html", page=page, character=player)
    
    elif page["type"] == "one_choice":
        return render_template("one_choice.html", page=page, character=player)
    
    elif page["type"] == "two_choices":
        return render_template("two_choices.html", page=page, character=player)
    
    elif page["type"] == "combat_start":
        utils.loadMonster(page)
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

    playerAttack = diceroll.twoDsix() + player.skill
    monsterAttack = diceroll.twoDsix() + monster.skill
    if playerAttack >= monsterAttack:
        monster.setHealth(monster.health - 2)
        playerWin = True
    else:
        player.setHealth(player.health - 2)
        playerWin =False

    if monster.health <= 0:
        session['in_combat'] = False
        monster.clearMonster()
        return render_template("combat_won.html", character=player, monster=monster, playerAttack=playerAttack, monsterAttack=monsterAttack)
    elif player.health <= 0:
        session['in_combat'] = False
        return render_template("you_died.html")
    else:
        return render_template("combat.html", character=player, monster=monster, playerWin=playerWin, playerAttack=playerAttack, monsterAttack=monsterAttack)
     
@views.route('/potion', methods=["POST"])
def potion():
    player = Player()
    player.getPlayer()
    inCombat = session['in_combat']

    if player.health == player.initHealth:
        canPotion = "max_health"
    elif player.potions > 0:
        canPotion = "has_potions"
        potions = player.potions - 1
        player.setPotions(potions)
        player.setHealth(player.initHealth)
    else:
        canPotion = "no_potions"
    return render_template("used_potion.html", character=player, canPotion=canPotion, inCombat=inCombat)