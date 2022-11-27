from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO,emit

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ama.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc85zkjAAAAAKtAs2TDJ30hfDz5Jua2ENVdbSXL'
app.config['RECAPTCHA_SECRET_KEY'] = '6Lc85zkjAAAAAMky8wx35BKqFuKWSfj82Ryf4gJD'
socketio = SocketIO(app,engineio_logger=True, logger=True)
socketio.init_app(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_message = 'Harap login untuk melihat direktori ini!'
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from ama import routes
