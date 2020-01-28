from flask import Flask
from .database import init_db
from .config import Config
import os
from .models import models
from flask_login import LoginManager




def create_app():
  app = Flask(__name__)
  login_manager = LoginManager()
  login_manager.init_app(app)
  app.config.from_object(Config)
  app.secret_key = os.urandom(24)
  init_db(app)
  return app

app = create_app()
