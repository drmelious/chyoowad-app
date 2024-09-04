from server import create_app
from flask import json

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)