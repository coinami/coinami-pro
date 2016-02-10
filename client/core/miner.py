# This module is going to be the client miner interface.
# Client will be able to request work from servers who are authorities.
# Client can also watch process of the work in stages. For example:
# Requesting Work -> Downloading Work -> Mining -> Uploading Results -> Accepted!
# Client should know which works it has done and when.
# Client can cancel works or pause them. Mining stage may not be able to be paused. 

# Basic needs : HTTP File Download and Upload, HTTP request. Keep track of works on the computer. Works may not be written into local database, instead just keep them in files.
import copy
import custom
import json
import subprocess
import sys
import time
import tools

miner_process = None


# Creates the coinbase transactions
def make_mint(pubkey):
    address = tools.make_address([pubkey], 1)
    return {'type': 'mint',
            'pubkeys': [pubkey],
            'signatures': ['first_sig'],
            'count': tools.count(address, custom.queues)}


# Creates the first block in chain
def genesis(pubkey):
    out = {'version': custom.version,
           'length': 0,
           'time': time.time(),
           'txs': [make_mint(pubkey)]}
    out = tools.unpackage(tools.package(out))
    return out


# Packages the current possible block scheme to get ready for mining
def make_block(prev_block, txs, pubkey):
    leng = int(prev_block['length']) + 1

    out = {'version': custom.version,
           'txs': txs,  # dont forget to add coinbase transaction ;)
           'length': leng,
           'time': time.time(),
           'prevHash': tools.det_hash(prev_block)}
    out = tools.unpackage(tools.package(out))
    return out


def insert_block(pubkey, rewarded_pubkey):
    length = tools.db_get('length')

    if length == -1:
        # this is the first ever block
        candidate_block = genesis(pubkey)
    else:
        # get the last block
        prev_block = tools.db_get(length)
        candidate_block = make_block(prev_block, tools.db_get('txs'), pubkey)

    txs = copy.deepcopy(candidate_block['txs'])
    flag = True
    for tx in txs:
        if tx['type'] == 'mint':
            # no need to add reward
            flag = False
    if flag:
        txs = txs + [make_mint(rewarded_pubkey)]
        candidate_block['txs'] = txs

    if tools.db_existence('privkey'):
        privkey = tools.db_get('privkey')
    else:
        return 'no private key is known, so the tx cannot be signed. Here is the tx: \n' + str(
                tools.package(txs).encode('base64').replace('\n', ''))

    candidate_block['auth_sign'] = tools.sign(tools.det_hash(candidate_block), privkey)
    candidate_block['auth_pubkey'] = pubkey

    if candidate_block is None:
        return
    else:
        custom.queues['suggested_blocks'].put(candidate_block)


# The variables are initialized and mining can begin!
# The most important part for mediator interface it that the executable which is given to our coin interface should meet the following constraints
# 1. It must have start with ./exe start <pubkey>
# 2. It must tell the status of the job with stdio. Program should update the status by writing to the stdio.
# 3. When it is finished, if the work is done, program should return 0. 
def mine_client(pubkey):
    def readable_time(mytime):
        return time.strftime("%D %H:%M", time.localtime(int(mytime)))

    print 'client miner started'
    executable = copy.deepcopy(custom.client_executable)
    executable.append(pubkey)
    miner_process = subprocess.Popen(executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print executable
    tools.db_put('miner_id', miner_process.pid)

    while True:
        nextline = miner_process.stdout.readline()
        if miner_process.poll() is not None:
            break
        nextline = nextline.rstrip('\n')
        try:
            status = json.loads(nextline)[u'status']
            tools.db_put('miner_status', status)
            tools.db_put('minestatustext',
                         readable_time(time.time()) + '  ' + status + '\n' + tools.db_get('minestatustext'))
        except:
            pass

    # wait for process to actually finish
    returncode = miner_process.poll()
    tools.db_put('miner_id', -1)

    if returncode == 0:
        print 'Mining is done succesfully'
    else:
        print 'Mining is finished prematurely.'

    tools.db_put('mine', False)


# The variables are initialized and mining can begin!
def mine_server(pubkey):
    print 'server miner started'
    executable = custom.server_executable
    miner_process = subprocess.Popen(executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tools.db_put('miner_id', miner_process.pid)

    while True:
        nextline = miner_process.stdout.readline()
        if miner_process.poll() != None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()
        nextline = nextline.rstrip('\n')
        if nextline != '':
            insert_block(pubkey, nextline)

    # wait for process to actually finish
    tools.db_put('miner_id', -1)
    print 'Mining is ended'
    tools.db_put('mine', False)


def main(pubkey):
    try:
        while True:
            custom.queues['heart_queue'].put('miner')
            if tools.db_get('stop'):
                tools.log('shutting off miner')
                return
            # if mining is open
            elif tools.db_get('mine'):
                if tools.is_authority(pubkey=tools.db_get('pubkey')):
                    mine_server(pubkey)
                else:
                    mine_client(pubkey)
            else:
                time.sleep(1)
    except Exception as exc:
        print 'miner main gave an exception', str(exc)
        tools.log('miner main: ')
        tools.log(exc)
