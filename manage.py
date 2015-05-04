__author__ = 'mizumoto'

from flask.ext.script import Manager, Server
from app import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='localhost',
    port=8888)
)


if __name__ == "__main__":
    manager.run()