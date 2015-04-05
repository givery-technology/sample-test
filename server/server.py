from app import app
use_reloader = app.config['USE_RELOADER']
port = app.config['PORT']
app.run(use_reloader=use_reloader, port=port)