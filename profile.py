import time

from helpers import get_last_blocks, get_last_blocks_threaded


def profile_get_last_blocks():
    # synchronous
    start = time.time()
    get_last_blocks(10)
    print(time.time() - start)

    # threaded
    start = time.time()
    get_last_blocks_threaded(10)
    print(time.time() - start)

profile_get_last_blocks()
