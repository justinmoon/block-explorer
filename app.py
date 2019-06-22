from flask import Flask, redirect, render_template, request, url_for

from explorer import get_block_with_txns, get_last_blocks_threaded, get_tx, rpc

app = Flask(__name__)


def handle_search(query):
    if query.isdigit():
        blockhash = rpc.getblockhash(int(query))
        return redirect(url_for(".block", blockhash=blockhash))
    elif query.startswith("0000"):
        return redirect(url_for(".block", blockhash=query))
    elif len(query) == 64:
        return redirect(url_for(".tx", tx_id=query))
    elif 25 < len(query) < 35:
        print("can't handle addresses yet")
        return redirect(".index")
    else:
        print("invalid input")
        return redirect(".index")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("Form submitted", request.form)
        query = request.form.get("query").strip()
        return handle_search(query)
    blocks = get_last_blocks_threaded(10)
    return render_template("index.html", blocks=blocks)


@app.route("/block/<blockhash>")
def block(blockhash):
    block = get_block_with_txns(blockhash)
    return render_template("block.html", block=block)


@app.route("/tx/<tx_id>")
def tx(tx_id):
    tx = get_tx(tx_id)
    return render_template("tx.html", tx=tx)


if __name__ == "__main__":
    app.run(debug=True)
