"""We regularly check on peers to see if they have mined new blocks.
This file explains how we initiate interactions with our peers.
"""
import blockchain
import custom
import networking
import random
import time
import tools

import numpy as np


def network_cmd(peer, x):
    return networking.send_command(peer, x)


def download_blocks(peer, peers_block_count, length):
    b = [max(0, length - 10), min(peers_block_count['length'] + 1, length + custom.download_many)]

    # tell them our request's range
    blocks = network_cmd(peer, {'type': 'rangeRequest', 'range': b})

    if type(blocks) != list: return -1

    if not isinstance(blocks, list): return []

    length = tools.db_get('length')  # our blockcount
    block = tools.db_get(length)  # get the last block

    for i in range(10):  # this part should be re-written so badly -> this was from Zack.... NO COMMENT
        if tools.fork_check(blocks, custom.queues, length, block):  # if block is valid
            blockchain.delete_block(custom.queues)  # wtf does this do?
            length -= 1

    for block in blocks:
        custom.queues['suggested_blocks'].put([block, peer])

    return 0


def ask_for_txs(peer):
    txs = network_cmd(peer, {'type': 'txs'})
    if not isinstance(txs, list):
        return -1
    for tx in txs:
        custom.queues['suggested_txs'].put(tx)
    T = tools.db_get('txs')
    pushers = filter(lambda t: t not in txs, T)
    for push in pushers:
        network_cmd(peer, {'type': 'pushtx', 'tx': push})
    return 0


def give_block(peer, block_count_peer):
    blocks = []
    b = [max(block_count_peer - 5, 0), min(tools.db_get('length'), block_count_peer + custom.download_many)]
    for i in range(b[0], b[1] + 1):
        blocks.append(tools.db_get(i, custom.queues))
    network_cmd(peer, {'type': 'pushblock',
                       'blocks': blocks})
    return 0


# main function for checking peers.
def peer_check(i, peers):
    peer = peers[i][0]
    # request their blockcount
    block_count = network_cmd(peer, {'type': 'blockCount'})
    if not isinstance(block_count, dict):
        return
    if 'error' in block_count.keys():
        return

    peers[i][2] = block_count['length']

    # tools.db_put('peers_ranked', peers)
    us_length = tools.db_get('length')
    their_length = block_count['length']

    # simple, if we are ahead, we give them our blocks
    if their_length < us_length:
        give_block(peer, custom.queues, their_length)
    elif their_length == us_length:
        # If we are at the same amount of block, we ask for new transaction they know
        try:
            ask_for_txs(peer, custom.queues)
        except Exception as exc:
            tools.log('ask for tx error')
            tools.log(exc)
    # request blocks
    # we are back
    else:
        download_blocks(peer, custom.queues, block_count, us_length)

    F = False

    # Send and receive peers
    my_peers = tools.db_get('peers_ranked')
    their_peers = network_cmd(peer, {'type': 'peers'})

    if type(their_peers) == list:
        for p in their_peers:
            if p not in my_peers:
                F = True
                my_peers.append(p)

        for p in my_peers:
            if p not in their_peers:
                network_cmd(peer, {'type': 'recieve_peer', 'peer': p})

    if F:
        my_peers = np.array(my_peers)
        tools.update_peers(my_peers[:, 0])

    return 0


def exponential_random(r, i=0):
    if random.random() < r: return i
    return exponential_random(r, i + 1)


def main(peers):
    # Check on the peers to see if they know about more blocks than we do.

    p = tools.db_get('peers_ranked')

    if type(p) != list:
        time.sleep(3)
        return main(peers, custom.queues)

    tools.update_peers(peers)

    try:
        while True:
            if tools.db_get('stop'):
                return
            if len(peers) > 0:
                # If we find at least one peer, we call the main_once method
                main_once(custom.queues)
    except Exception as exc:
        tools.log(exc)


def main_once():
    # put the peers check in heart queue.
    custom.queues['heart_queue'].put('peers check')

    # sort by rank in decreasing order
    peers = tools.db_get('peers_ranked')
    peers = sorted(peers, key=lambda r: r[2])
    peers.reverse()

    time.sleep(0.05)

    if custom.queues['suggested_blocks'].empty():
        time.sleep(2)

    i = 0
    # wait while suggested blocks are not empty
    # they are needed to be taken care of
    while not custom.queues['suggested_blocks'].empty() and not tools.db_get('stop'):
        i += 1
        time.sleep(0.1)
        if i % 100 == 0:
            custom.queues['heart_queue'].put('peers check')

    if tools.db_get('stop'):
        return

    custom.queues['heart_queue'].put('peers check')
    peer_id = exponential_random(3.0 / 4) % len(peers)
    t1 = time.time()
    r = peer_check(peer_id, peers, custom.queues)
    t2 = time.time()
    a_peer = peers[peer_id][0]

    peers = tools.db_get('peers_ranked')
    for peer in peers:
        if peer[0] == a_peer:
            peers[peer_id][1] *= 0.8
            if r == 0:
                peers[peer_id][1] += 0.2 * (t2 - t1)
            else:
                peers[peer_id][1] += 0.2 * 30

    tools.db_put('peers_ranked', peers)
    custom.queues['heart_queue'].put('peers check')
