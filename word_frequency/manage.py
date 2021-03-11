from flask import Flask
import logging

app = Flask(__name__,template_folder='./templates',static_folder='./static')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .views import user
from .views import audio

app.register_blueprint(user.us)
app.register_blueprint(audio.au)

