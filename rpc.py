import ssl
import toml
import threading
import os

from flask import current_app, request
from bitcoinrpc.authproxy import AuthServiceProxy


class RPCWrapper:
    
    template = "{TRANSPORT}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    settings = toml.load('settings.toml')
    
    def __init__(self, node):
        self.node = node

    def proxy(self, network):
        settings = self.settings[self.node][network]
        url = self.template.format(**settings)
        return AuthServiceProxy(url, context=self.context())

    def context(self):
        if self.node == 'btcd':
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            context = None
        return context

    def __getattr__(self, name):
        """Hack to establish a new AuthServiceProxy every time this is called"""
        if current_app and 'testnet' in request.path:
            network = 'testnet'
        else:
            network = 'mainnet'
        print('calling', network, name)
        return getattr(self.proxy(network), name)



rpc = RPCWrapper(os.environ.get('NODE', 'bitcoind'))


def get_block(x):
    if isinstance(x, int):
        blockhash = rpc.getblockhash(x)
    else:
        blockhash = x
    return rpc.getblock(blockhash)


def get_block_with_txns(blockhash):
    if rpc.node == 'bitcoind':
        return rpc.getblock(blockhash, 2)
    else:
        r = rpc.getblock(blockhash, True, True)
        r['tx'] = r.pop('rawtx')
        return r


def get_blocks_threaded(height, num_blocks):
    def get_block_threaded(blocks, i):
        blockhash = rpc.getblockhash(height - i)
        block = rpc.getblock(blockhash)
        blocks[i] = block

    blocks = [None] * num_blocks
    threads = [None] * num_blocks

    for i in range(len(threads)):
        threads[i] = threading.Thread(target=get_block_threaded, args=(blocks, i))
        threads[i].start()

    for thread in threads:
        thread.join()

    return blocks


def get_last_blocks_threaded(num_blocks):
    height = rpc.getblockchaininfo()["blocks"]
    return get_blocks_threaded(height, num_blocks)


def get_last_blocks(num_blocks):
    """get `num_blocks` starting from `height`"""
    blocks = []
    blockhash = rpc.getbestblockhash()
    for _ in range(num_blocks):
        block = rpc.getblock(blockhash)
        blockhash = block["previousblockhash"]
        blocks.append(block)
    return blocks


def get_tx(tx_id):
    # btcd demands an integer
    # TODO: explore this and patch either python-jsonrpc or btcd ...
    return rpc.getrawtransaction(tx_id, 1)  


def get_tx_with_inputs(tx_id):
    tx = get_tx(tx_id)
    for i, vin in enumerate(tx["vin"]):
        # Ignore coinbases
        if "coinbase" not in vin:
            t = get_tx(vin["txid"])
            utxo = t["vout"][vin["vout"]]
            vin["spending"] = utxo
    return tx


def get_tx_for_address(address):
    return rpc.searchrawtransactions(address)
