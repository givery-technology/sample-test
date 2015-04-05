class Config(object):
    # SQL connection URI
    SQLALCHEMY_DATABASE_URI = 'mysql://cody:cody@localhost/cody'
    # Listening port
    PORT = 8888
    # Reload the application when the source code is modified
    USE_RELOADER = True
    # Print debug information
    DEBUG = True
