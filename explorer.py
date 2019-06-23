import threading

from rpc import RPC

rpc = RPC()


def get_block(blockhash):
    return rpc.getblock(blockhash)


def get_block_with_txns(blockhash):
    return rpc.getblock(blockhash, 2)


def get_blocks_threaded(height, num_blocks):
    def get_block_threaded(blocks, i):
        blockhash = rpc.getblockhash(height - i)
        print(f"fetching {blockhash}")
        block = rpc.getblock(blockhash)
        blocks[i] = block

    blocks = [None] * 10
    threads = [None] * 10
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
    return rpc.getrawtransaction(tx_id, True)


def get_tx_with_inputs(tx_id):
    tx = get_tx(tx_id)
    for i, vin in enumerate(tx["vin"]):
        # Ignore coinbases
        if "coinbase" not in vin:
            t = get_tx(vin["txid"])
            t_out = t["vout"][i]
            vin["spending"] = t_out
    return tx
