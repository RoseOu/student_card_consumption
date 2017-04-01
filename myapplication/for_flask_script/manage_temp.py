from flask_script import Manager

from myapp import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()

@manager.option('-n', '--name', help='Your name')
def hello(name):
    print "hello", name

#You can override this list in sub-commands and -managers:

def talker(host='localhost'):
    pass
ccmd = ConnectCmd(talker)
ccmd.help_args = ('-?', '--help')
manager.add_command("connect", ccmd)
manager.run()
python manage.py hello --name=Joe
hello Joe

#To facilitate this you use the option_list attribute of the Command class:

from flask_script import Command, Manager, Option

class Hello(Command):

    option_list = (
        Option('--name', '-n', dest='name'),
    )

    def run(self, name):
        print "hello %s" % name

#Alternatively, you can define a get_options method 
#for your Command class. This is useful if you want 
# to be able to return options at runtime based on 
# for example per-instance attributes:

class Hello(Command):

    def __init__(self, default_name='Joe'):
        self.default_name=default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        print "hello",  name
@manager.command
def hello(name):
    print "hello", name
The @command decorator is fine for simple operations, 
but often you need the flexibility. For more 
sophisticated options it’s better to use the @option decorator:

@manager.option('-n', '--name', dest='name', default='joe')
def hello(name):
    print "hello", name
You can add as many options as you want:

@manager.option('-n', '--name', dest='name', default='joe')
@manager.option('-u', '--url', dest='url', default=None)
def hello(name, url):
    if url is None:
        print "hello", name
    else:
        print "hello", name, "from", url
