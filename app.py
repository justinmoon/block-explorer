from flask import Flask

from blueprint import blueprint

app = Flask(__name__)

app.register_blueprint(blueprint)
app.register_blueprint(blueprint, url_prefix='/testnet')

if __name__ == "__main__":
    app.run()
