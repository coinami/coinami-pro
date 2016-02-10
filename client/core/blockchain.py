""" This file explains explains the rules for adding and removing blocks from the local chain.
"""
import time
import copy
import custom
import networking
import transactions
import tools


# This function's purpose is to add the tx to the database.
# It is used when adding orphan transactions to database. 
# It also is used when adding ordinary transactions to database.
def add_tx(tx):
    # Attempt to add a new transaction into the pool.

    out = ['']
    # check tx variable's type
    if type(tx) != type({'a': 1}):
        return False

    # make address from pubkeys and signatures of transaction
    address = tools.make_address(tx['pubkeys'], len(tx['signatures']))

    def verify_count(tx, txs):
        return tx['count'] != tools.count(address)

    def type_check(tx, txs):
        if not tools.E_check(tx, 'type', [str, unicode]):
            out[0] += 'Blockchain type'
            return False

        # mint type cannot be added to database
        if tx['type'] == 'mint':
            return False

        # type is not recognized
        if tx['type'] not in transactions.tx_check:
            out[0] += 'Bad type'
            return False

        return True

    def too_big_block(tx, txs):
        return len(tools.package(txs + [tx])) > networking.MAX_MESSAGE_SIZE - 5000

    def verify_tx(tx, txs, out):
        # check if the type of transaction lets you add the transaction back to database
        if not type_check(tx, txs):
            out[0] += 'Type error\n'
            return False
        if tx in txs:
            out[0] += 'No duplicates\n'
            return False
        # is this transaction possible with this count
        if verify_count(tx, txs):
            out[0] += 'Count error\n'
            return False
        # this block cannot be sent over network
        if too_big_block(tx, txs):
            out[0] += 'Too many txs\n'
            return False
        # run the last tx_check test from transactions module
        if not transactions.tx_check[tx['type']](tx, txs, out):
            out[0] += 'Transaction was not verified!\n'
            return False
        return True

    txs_from_db = tools.db_get('txs')

    if verify_tx(tx, txs_from_db, out):

        txs_from_db.append(tx)
        tools.db_put('txs', txs_from_db)
        return ('Added transaction with %d amount to %s' % (tx['amount'], tx['to']))

    else:
        return ('Failed to add tx because: \n' + out[0])


# gets the key, size and length
# 
def recent_blockthings(key, size, length=0):
    # get the storage from DB which was originally recorded as "key"
    storage = tools.db_get(key)

    def get_val(length):
        leng = str(length)
        if not leng in storage:
            block = tools.db_get(leng)
            if block == database.default_entry():
                if leng == tools.db_get('length'):
                    tools.db_put('length', int(leng) - 1)
                    block = tools.db_get(leng)

            # try:
            storage[leng] = tools.db_get(leng)[key[:-1]]
            tools.db_put(key, storage)
        return storage[leng]

    # pop from storage till you reach the end
    def clean_up(storage, end):
        if end < 0: return
        if not str(end) in storage:
            return
        else:
            storage.pop(str(end))
            return clean_up(storage, end - 1)

    # DB returns the blockchain length from 'length' key
    if length == 0:
        length = tools.db_get('length')

    start = max((length - size), 0)
    clean_up(storage, length - max(custom.mmm, custom.history_length) - 100)
    return map(get_val, range(start, length))


def hexSum(a, b):
    # Sum of numbers expressed as hexidecimal strings
    return tools.buffer_(str(hex(int(a, 16) + int(b, 16)))[2: -1], 64)


def hexInvert(n):
    # Use double-size for division, to reduce information leakage.
    return tools.buffer_(str(hex(int('f' * 128, 16) / int(n, 16)))[2: -1], 64)


def add_block(block_pair):
    """Attempts adding a new block to the blockchain.
     Median is good for weeding out liars, so long as the liars don't have 51%
     hashpower. """

    def median(mylist):
        if len(mylist) < 1:
            return 0
        return sorted(mylist)[len(mylist) / 2]

    def block_check(block):

        def log_(txt):
            pass  # return tools.log(txt)

        def check_txs(txs):

            start = copy.deepcopy(txs)
            out = []
            start_copy = []

            # until starting copy of transactions are empty
            while start != start_copy:
                if start == []:
                    return False  # Block passes this test

                start_copy = copy.deepcopy(start)

                # if transaction is valid, then add the transaction to the out list
                if transactions.tx_check[start[-1]['type']](start[-1], out, ['']):
                    out.append(start.pop())

                else:
                    return True  # Block is invalid

            return True  # Block is invalid

        # if block is not a dict, return false
        if not isinstance(block, dict): return False

        # block contains error
        if 'error' in block: return False

        # E_check function is responsible for checking the block(dict) if it has a length attribute which is int
        if not tools.E_check(block, 'length', [int]):
            log_('no length')
            return False

        # get the length of blockchain
        length = tools.db_get('length')

        # check length if it is integer, yeah yeah we have done that so what?
        if type(block['length']) != type(1):
            log_('wrong length type')
            return False

        # check length condition. It must be one bigger than our current blockchain length, or we would be missing something
        if int(block['length']) != int(length) + 1:
            log_('wrong longth')
            return False

        # checking if prevHash was actually the previous block's hash
        if length >= 0:
            if tools.det_hash(tools.db_get(length)) != block['prevHash']:
                log_('det hash error')
                return False

        # --------------------- START OF THE NEW PROOF-OF-WORK CHECK---------------------------------

        # Returns a dictionary with auth_sign and halfHash of block.
        # Authority must sign the block with its pubkey. This way, we are going to know which authority signed the block
        half_way = tools.make_half_way(block)
        if not half_way.get('auth_pubkey') in tools.db_get('authorities'):
            print 'no auth pubkey'
            return False

        if not tools.verify(half_way.get('halfHash'), half_way.get('auth_sign'), half_way.get('auth_pubkey')):
            print 'no verify'
            return False

        # --------------------- END OF THE NEW PROOF-OF-WORK CHECK-----------------------------------

        # recent_blockthings returns a map with get_val function and range starting from 100 early blocks to most recent block
        # then earliest is the median of sorted blocks
        earliest = median(recent_blockthings('times', custom.mmm))

        # time has to be present in block
        if 'time' not in block:
            log_('no time')
            return False

        # it is late to check this block
        if block['time'] > time.time() + 60 * 6:
            log_('too late')
            return False

        # block does not seem to be created at correct time
        if block['time'] < earliest:
            log_('too early')
            return False

        # check the transactions in the block
        # this function returns True on negative situation, because fuck the logic!
        # please someone fix this. I left it for now to show how a joken source this project is!
        if check_txs(block['txs']):
            log_('tx check')
            return False

        return True

    # This is where the add_block logic begins

    # if the block_pair is an array
    if type(block_pair) == type([1, 2, 3]):
        # block is actually the first element
        block = block_pair[0]
        # peer is the second element
        peer = block_pair[1]
    else:
        block = block_pair
        peer = False

    # block_check takes two inputs : block and current DB
    # it runs many tests on block including transactions and other things
    if block_check(block):
        # update the database with new block
        tools.db_put(block['length'], block)
        tools.db_put('length', block['length'])
        orphans = tools.db_get('txs')
        tools.db_put('txs', [])
        for tx in block['txs']:
            # update the database with this new transaction.
            transactions.update[tx['type']](tx, True)
        # add all orphan transactions back to database
        for tx in orphans:
            add_tx(tx)


def delete_block(DB):
    """ Removes the most recent block from the blockchain. """
    length = tools.db_get('length')
    if length < 0:
        return

    try:
        ts = tools.db_get('times')
        ts.pop(str(length))
        tools.db_put('times', ts)
    except:
        pass
    block = tools.db_get(length, DB)
    orphans = tools.db_get('txs')
    tools.db_put('txs', [])
    for tx in block['txs']:
        orphans.append(tx)
        tools.db_put('add_block', False)
        transactions.update[tx['type']](tx, DB, False)
    tools.db_delete(length, DB)
    length -= 1
    tools.db_put('length', length)
    if length == -1:
        tools.db_put('diffLength', '0')
    else:
        block = tools.db_get(length, DB)
    for orphan in sorted(orphans, key=lambda x: x['count']):
        add_tx(orphan, DB)
        # while tools.db_get('length')!=length:
        #    time.sleep(0.0001)


def manage_queues(blocks_queue, txs_queue):
    def is_blocks_queue_empty():
        return blocks_queue.empty()

    def is_txs_queue_empty():
        return txs_queue.empty()

    def add_from_queue(queue, add_function, is_queue_empty, queue_name):
        # while the queue is not empty, in other words there are suggested blocks or transactions, call the corresponding add function
        while not is_queue_empty():
            time.sleep(0.0001)
            try:
                add_function(queue.get(False))
            except Exception as exc:
                tools.log('suggestions ' + queue_name)
                tools.log(exc)

    # start the loop until it gets stopped
    while True:
        time.sleep(0.1)
        if tools.db_get('stop'):
            # Free the queues
            tools.dump_out(blocks_queue)
            tools.dump_out(txs_queue)
            return
        while not is_blocks_queue_empty() or not is_txs_queue_empty():
            add_from_queue(blocks_queue, add_block, is_blocks_queue_empty, 'block')
            add_from_queue(txs_queue, add_tx, is_txs_queue_empty, 'tx')


import cProfile


# threads.py calls this function.
# It calls the manage_queues with suggested blocks and txs
def main(): return manage_queues(custom.queues["suggested_blocks"], custom.queues["suggested_txs"])
