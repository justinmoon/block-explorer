import threading, os

from rpc import RPCRouter


rpc = RPCRouter(os.environ.get('NODE', 'bitcoind'))


def get_block(blockhash):
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


def get_blocks(height, num_blocks):
    """get `num_blocks` starting from `height`"""
    blocks = []
    next_block_hash = rpc.getblockhash(height)
    for _ in range(num_blocks):
        block = get_block(next_block_hash)
        next_block_hash = block["previousblockhash"]
        blocks.append(block)
    return blocks


def get_last_blocks(num_blocks):
    height = rpc.getblockchaininfo()["blocks"]
    return get_blocks(height, num_blocks)


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
