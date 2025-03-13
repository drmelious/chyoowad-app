from server import create_app
import os

os.environ['CONFIG_TYPE'] = 'config.NotTestingConfig'
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)