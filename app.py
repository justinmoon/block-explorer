from datetime import datetime

from flask import Flask

from blueprint import blueprint
from moment import format_unixtime

app = Flask(__name__)

app.jinja_env.globals['format_unixtime'] = format_unixtime
app.register_blueprint(blueprint)
app.register_blueprint(blueprint, url_prefix='/testnet')

if __name__ == "__main__":
    app.run()
