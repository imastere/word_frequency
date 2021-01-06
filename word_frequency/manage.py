from flask import Flask

app = Flask(__name__)

from .views import user

app.register_blueprint(user.us)
