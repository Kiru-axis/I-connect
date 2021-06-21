from app import create_app,db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Subscriber, User #Userclass



app = create_app('development')
app = create_app('test')
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)



@manager.shell
def make_shell_context():
  return dict(app = app,db = db,User = User)
# running unittests
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=4).run(tests)



if __name__ == '__main__':
  manager.run()