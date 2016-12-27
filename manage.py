import os
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
# from livereload import Server


from app import create_app , db
from flask.ext.script import Manager , Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import Content,User

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,db=db,Content=Content,User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    app.run(debug=True)
    # server = Server(app.wsgi_app)
    # server.serve(  )
   # manager.run()


