import os
from flask import Flask
from flask_bootstrap import Bootstrap

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


if __name__ == "__main__":
	host = os.popen('hostname -I').read()
	app.run(host=host, port=80, debug=True)

from app import routes