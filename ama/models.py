from ama import db,bcrypt,login_manager
from flask_login import UserMixin,login_user


# load user info from database when user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_login(username,password):
    attemptedUser = search_user(username)
    if attemptedUser and attemptedUser.check_password_correction(attempted_password=password):
        login_user(attemptedUser)
        return(f"Selamat datang {attemptedUser.username}!", 200)
    return(['Username atau password salah!, harap coba kembali.'], 400)

def generate_bgcolor():
    last_user_bg = Message.query.filter().order_by(Message.id.desc()).first().bg_color
    bgcolor = ['bg-primary','bg-secondary','bg-success','bg-danger','bg-warning','bg-info','bg-dark']
    bg_index = bgcolor.index(last_user_bg)
    if bg_index < len(bgcolor)-1:
        return bgcolor[bg_index+1]
    return bgcolor[0]

def search_user(value):
    if '@' in value:
        return User.query.filter_by(email_address=value).first()
    return User.query.filter_by(username=value).first()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30),nullable=False)
    email = db.Column(db.String(length=30),nullable=False)
    password_hash = db.Column(db.String(length=30),nullable=False)
    messages = db.relationship('Message', backref='user')
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password): #function to encrypt password when user register on this websites
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password): #function to check password when user try to login.
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def to_dict(self):
        return {'username':self.username,'email':self.email}

class Message(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    message = db.Column(db.String(),nullable=False)
    bg_color = db.Column(db.String(length=20),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_dict(self):
        return {'messages':self.messages,'bg_color':self.bg_color}