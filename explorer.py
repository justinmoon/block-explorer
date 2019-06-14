from rpc import RPC

rpc = RPC()

def get_blocks(height, num_blocks):
    """get `num_blocks` starting from `height`"""
    blocks = []
    next_block_hash = rpc.getblockhash(height)
    for _ in range(num_blocks):
        block = rpc.getblock(next_block_hash)
        next_block_hash = block["previousblockhash"]
        blocks.append(block)
    return blocks

def get_tx(tx_id):
    return rpc.getrawtransaction(tx_id, True)

if __name__ == "__main__":
    tx_id = "f9fbb483821735103d0c7c2ce2771a09bb1e20731d17c6e8ae204623a9dc0b10"
    print(get_tx(tx_id))
