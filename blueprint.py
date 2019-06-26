from bitcoinrpc.authproxy import JSONRPCException
from flask import Blueprint, redirect, render_template, request, url_for
from helpers import (get_block_with_txns, get_last_blocks_threaded,
                     get_tx_with_inputs, rpc, get_tx_for_address, get_last_blocks)

blueprint = Blueprint('explorer', __name__, 
        static_folder='static', template_folder='templates')

@blueprint.errorhandler(ConnectionRefusedError)
def handle_connection_refused(e):
    return redirect(url_for(".error", msg="bitcoin RPC failed"))


@blueprint.errorhandler(JSONRPCException)
def handle_rpc_error(e):
    return redirect(url_for(".error", msg=e.message))


def handle_search(query):
    if query.isdigit():
        blockhash = rpc.getblockhash(int(query))
        return redirect(url_for(".block", blockhash=blockhash))
    elif query.startswith("0000"):
        return redirect(url_for(".block", blockhash=query))
    elif len(query) == 64:
        return redirect(url_for(".tx", tx_id=query))
    elif 25 < len(query) < 35:
        return redirect(url_for(".address", address=query))
    else:
        # we should display some kind of error ...
        print("invalid input")
        return redirect(url_for(".error", msg="No results found"))


@blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query").strip()
        return handle_search(query)
    blocks = get_last_blocks(5)
    return render_template("index.html", blocks=blocks)


@blueprint.route("/block/<blockhash>")
def block(blockhash):
    block = get_block_with_txns(blockhash)
    return render_template("block.html", block=block)


@blueprint.route("/tx/<tx_id>")
def tx(tx_id):
    tx = get_tx_with_inputs(tx_id)
    return render_template("tx.html", tx=tx)


@blueprint.route("/address/<address>")
def address(address):
    txns = get_tx_for_address(address)
    return render_template("address.html", address=address, txns=txns)


@blueprint.route("/error")
def error(msg=None):
    msg = request.args.get("msg")
    return render_template("error.html", msg=msg)
