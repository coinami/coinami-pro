"""This is to make magic numbers easier to deal with."""
import multiprocessing
import os

import pickledb

try:
    from cdecimal import Decimal
except:
    from decimal import Decimal
# These are pubkeys of authorities. We will use them to check new blocks

current_loc = os.path.dirname(os.path.abspath(__file__))
database_name = os.path.join(current_loc, 'database')
log_file = os.path.join(current_loc, 'log')
port = 7900
api_port = 7899
version = "0.0002"
max_key_length = 6 ** 4
block_reward = 10 ** 5
fee = 10 ** 3
conf_dir = os.path.expanduser('~/.coinami')
wallets_dir = os.path.expanduser('~/.coinami/Wallets')
conf_file = os.path.expanduser('~/.coinami/client.conf')

api_address = 'http://halilibo.com:7500'
info_address = 'http://halilibo.com:7500/info.json'
client_executable = ['python2', 'core/exe/client_executable.py']
server_executable = ['python2', 'core/exe/server_executable.py']

# Lower limits on what the "time" tag in a block can say.
mmm = 100
# Take the median of this many of the blocks.
# How far back in history do we look when we use statistics to guess at
# the current blocktime and difficulty.
history_length = 400
# This constant is selected such that the 50 most recent blocks count for 1/2 the
# total weight.
inflection = Decimal('0.985')
download_many = 100  # Max number of blocks to request from a peer at the same time.
max_download = 58000
blocktime = 60

processes = []
cmds = []

queues = {
    'reward_peers_queue': multiprocessing.Queue(),
    'suggested_blocks': multiprocessing.Queue(),
    'suggested_txs': multiprocessing.Queue(),
    'heart_queue': multiprocessing.Queue(),
}

db = pickledb.load(database_name, True)
