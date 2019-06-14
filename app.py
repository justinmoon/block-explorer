from flask import Flask, render_template
from explorer import get_block_with_txns, get_blocks

app = Flask(__name__)

@app.route('/')
def index():
    blocks = get_blocks(1000, 10)
    return render_template("index.html", blocks=blocks)

@app.route("/block/<blockhash>")
def block(blockhash):
    block = get_block_with_txns(blockhash)
    return render_template("block.html", block=block)

if __name__ == '__main__':
    app.run(debug = True)
