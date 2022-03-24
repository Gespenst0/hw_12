import logging

logging.basicConfig(filename="basic.log")

from flask import Flask, render_template
from main.views import main_blueprint
from loader.views import loader_blueprint

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)

app.run()