from flask import Flask, render_template
from explorer import get_blocks

app = Flask(__name__)

@app.route('/')
def index():
    blocks = get_blocks(1000, 10)
    return render_template("index.html", blocks=blocks)

if __name__ == '__main__':
    app.run(debug = True)
