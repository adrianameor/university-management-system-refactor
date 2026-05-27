from flask import Flask

from config import Config
from models import db, login_manager
from routes import init_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)