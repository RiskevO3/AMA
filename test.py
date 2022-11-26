from ama.models import db,User,Message

# db.drop_all()
# db.create_all()

# u = User(username='test',email='test',password='test')
# m = Message(name='anonymous',message='haloo',bg_color='bg-primary')
# u.messages.append(m)
# db.session.add_all([u,m])
# db.session.commit()

last_user_bg = Message.query.filter().order_by(Message.id.desc()).first().bg_color
print(last_user_bg)