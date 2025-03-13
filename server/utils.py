import json, os
from flask import session
from server.monster import Monster

def openBook():
    if os.environ['CONFIG_TYPE'] == 'config.TestingConfig':
        with open('server/books/test_book.json') as data:
            book = json.load(data)
    else:
        with open('server/books/first_steps.json') as data:
            book = json.load(data)
    return book

def loadNextPage(book, choice):
    currentPage = session['current_page']
    nextPage = book["pages"][currentPage]["options"][choice]["next_page"]
    page = book["pages"][nextPage]
    session['current_page'] = nextPage
    return page

def loadMonster(page):
    monster = Monster()
    monster.setMonster(page["monster"]["name"], page["monster"]["skill"], page["monster"]["health"])