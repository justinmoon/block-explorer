from rpc import RPC

rpc = RPC()

def get_block(blockhash):
    return rpc.getblock(blockhash)

def get_block_with_txns(blockhash):
    return rpc.getblock(blockhash, 2)

def get_blocks(height, num_blocks):
    """get `num_blocks` starting from `height`"""
    blocks = []
    next_block_hash = rpc.getblockhash(height)
    for _ in range(num_blocks):
        block = get_block_with_txns(next_block_hash)
        next_block_hash = block["previousblockhash"]
        blocks.append(block)
    return blocks

def get_last_blocks(num_blocks):
    height = rpc.getblockchaininfo()["blocks"]
    return get_blocks(height, num_blocks)

def get_tx(tx_id):
    return rpc.getrawtransaction(tx_id, True)

def search(query):
    if query.isdigit():
        print("block height")
    elif query.startswith("0000"):
        print("block hash")
    elif len(query) == 64:
        print("transaction")
    elif 25 < len(query) < 35:
        print("address")
    else:
        print("invalid input")

