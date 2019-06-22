from flask import Flask, render_template, request
from explorer import get_block_with_txns, get_last_blocks, get_tx, search

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("Form submitted", request.form)
        search(request.form.get('query'))
    blocks = get_last_blocks(3)
    return render_template("index.html", blocks=blocks)

@app.route("/block/<blockhash>")
def block(blockhash):
    block = get_block_with_txns(blockhash)
    return render_template("block.html", block=block)

@app.route("/tx/<tx_id>")
def tx(tx_id):
    tx = get_tx(tx_id)
    return render_template("tx.html", tx=tx)

if __name__ == '__main__':
    app.run(debug = True)
