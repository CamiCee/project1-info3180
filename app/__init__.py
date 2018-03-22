from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "d*xauhr3_=75%&!(w-$e=_(dr4ldd7p78t4jpxr7n9-#eq*&(t"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:compositionbook@localhost/project1"
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://snwrsyweqruemh:78217000d03a8e13303e883488233b14ddaa9e1eb738cceb81b9f533d7037e07@ec2-54-243-210-70.compute-1.amazonaws.com:5432/d6skuaqkm425rb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)
UPLOAD_FOLDER = './app/static/uploads'

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
