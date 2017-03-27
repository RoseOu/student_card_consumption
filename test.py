from flask_script import Manager
from flask import Flask

app = Flask(__name__)
manager = Manager(app)

@manager.command #这里用manager.command而不是addcommand
def hello():
    print "Hello, world"

if __name__ == "__main__":
    manager.run()