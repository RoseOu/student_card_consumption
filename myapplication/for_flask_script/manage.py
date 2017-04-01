from flask_script import Manager

from myapp import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

#使用方法:
#   @option decorator belong to Manager Class
#   used when you need more control over your 
#   command:
@manager.option('-n', '--name', help='Your name')
def hello(name):
    print "hello", name

#   2.0版本中-h所指向的命令有歧义，如果-h表示的是-help，那么就
#   无法使用-h来作为-host的参数。
#   如果你想还原-h的命令，你可以修改Manager类的help_args属性
manager = Manager()
manager.help_args = ('-h', 'help','-?')

#在sub—commands和-managers中重写这个列表
def talker(host='localhost'):
    pass
ccmd = ConnectCmd(talker)
ccmd.help_args = ('-?', '--help')
manager.add_command("connect", ccmd)
manager.run()
#有两种调用方法
#   manager -h 和 manager connect -help

#给命令添加参数
#   像下面这样:
#       $ python manager.py hello --name=Joe
#       >hello Joe
#       或者
#       $ python manager.py hello -n Joe
#为了让这个简化(facilitate)，使用Command类的option_list属性
from flask_script import Command, Manager, Option

class Hello(Command):
    option_list = (
        Option('--name', '-n', dest='name')
    )

    def run(self, name):
        print "hello %s" % name
#   位置和可选参数都以Option类的实例存储

#   你可以选择性的为你的Command类定义一个 get_options方法,如果
#   你希望在运行时基于每一个实例属性返回选项。
from flask_script import Command, Manager, Option

class Hello(Command):

    def __init__(self, default_name='Joe'):
        self.default_name=default_name
    
    def get_options(self):
        return [
            #dest – The name of the attribute to be added to the object returned by parse_args().
            #default – The value produced if the argument is absent from the command-line.
            Option('-n', '--name', dest='name', default=self.default_name), 
        ]
    def run(self, name):   #name就是get_options返回的option_list的dest
        print "hello", name
#   这里之所以设置一个get_options()和run()方法在API中是这样解释zhege
#   函数的：
#   class flask_script.Command(func=None)
#       get_options():return optional_list bydefault, override it if you need to do
#                     instance-specific configuration
#       run():需要子类来实现，需要从Command options中配置参数
#
# 
#  
     
#   如果你使用@command装饰器，那就更加容易了-这个options自
#   动从你的函数参数中提取，这是一个位置参数的例子
#   
@manager.command
def hello(name):
    print "hello", name
#   $python manager.py hello Joe  #Joe 就是位置参数
#   >hello Joe

#   @command装饰器在一些简单的操作下是很好用的
#   但是你经常需要灵活度更高的。对于那些相对复杂而精致的选项，
#   则用@option就更加好了
@manager.option('-n', '--name', dest='name', default='joe')
def hello(name):
    print "hello", name

#   随便添加多少命令都行
#   @option需要和Option类一样的参数
@manager.option('-n', '--name', dest='name', default='joe')
@manager.option('-u', '--url', dest='url', default=None)
def hello(name, url):
    if url is None:
        print 'hello', name
    else:
        print 'hello', name, 'from', url
#   调用方法 
#   > python manage.py hello -n Joe -u reddit.com
#   hello Joe from reddit.com
#   或者
#   > python manage.py hello --name=Joe --url=reddit.com
#   hello Joe from reddit.com




if __name__ == "__main__":
    manager.run()
