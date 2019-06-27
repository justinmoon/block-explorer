from datetime import datetime

from flask import Flask

from blueprint import make_blueprint
from moment import format_unixtime

app = Flask(__name__)

app.jinja_env.globals['format_unixtime'] = format_unixtime
app.register_blueprint(make_blueprint('mainnet'), url_prefix='/')
app.register_blueprint(make_blueprint('testnet'), url_prefix='/testnet')

if __name__ == "__main__":
    app.run()
