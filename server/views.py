from flask import Blueprint, render_template, request
import json

views = Blueprint('views', __name__)
currentPage = 0

@views.route('/', methods=["GET", "POST"])
def home():
    with open('server/static/first_steps.json') as data:
        book = json.load(data)
    global currentPage
    page=book["pages"][currentPage]
    currentPage = page["next_page"]
    return render_template("intro.html", page=page)
