from simple_script import User   #测试成功
from simple_script import db

db.create_all()

admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()