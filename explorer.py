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

if __name__ == "__main__":
    blocks = get_blocks(1000, 10)
