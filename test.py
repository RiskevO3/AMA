from ama.models import db,User

user = User.query.all()
print(user)