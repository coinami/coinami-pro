"""This program starts all the threads going. When it hears a kill signal, it kills all the threads.
"""
import api
import blockchain
import custom
import json
import miner
import multiprocessing
import networking
import peer_recieve
import peers_check
import sys
import time
import tools
import urllib2


def peer_recieve_func(d):
    return peer_recieve.main(d)


# This thread is started with start command from client module.
# @param brainwallet : brain wallet " seed " of the wallet.
# @param pubkey_flag : if brain wallet is actually pubkey
def main(wallet_name='', key=''):
    tools.log('custom.current_loc: ' + str(custom.current_loc))

    print('Starting Coinami Client ...')

    b = tools.db_existence('length')
    # Initialize the db
    if not b:
        tools.db_put('length', -1)
        tools.db_put('memoized_votes', {})
        tools.db_put('txs', [])
        tools.db_put('peers_ranked', [])
        tools.db_put('times', {})
        tools.db_put('mine', False)
        tools.db_put('peers', [])
        tools.db_put('authorities', [])
        tools.db_put('miner_status', 'Uninitialized')
        tools.db_put('miner_id', -1)
        tools.db_put('default_wallet', False)

    tools.db_put('stop', False)
    tools.log('stop: ' + str(tools.db_get('stop')))

    wallet = {}
    if key == '':
        wallet['valid'] = False
        wallet['message'] = 'Please define a passphrase to open the wallet'
    if wallet_name == '':
        wallet_name = tools.db_get('default_wallet')
        if not tools.db_get('default_wallet'):
            wallet['valid'] = False
            wallet['message'] = 'There is no defined default wallet. You need to specify one.'
        else:
            wallet = tools.read_wallet(wallet_name, key)

    elif wallet_name != '':
        wallet = tools.read_wallet(wallet_name, key)

    if not wallet['valid']:
        print wallet['message']
        sys.exit(0)

    # Take the initial peer and authority list over here. Also a download link for executable. 
    # Download can be started when miner is opened for the first time.
    # Peers and authorities must be set immediately.

    seed = str(wallet['seed'])
    try:
        info = json.loads(urllib2.urlopen(custom.info_address).read())
    except:
        print 'Could not read info file'
        sys.exit(0)

    peers = []
    for authority in info['authorities']:
        peers.append([authority['ip'], authority['port']])

    authorities = []
    for authority in info['authorities']:
        authorities.append(authority['pubkey'])

    tools.db_put('seed', seed)
    tools.db_put('info', info)
    tools.db_put('peers', peers)
    tools.db_put('authorities', authorities)
    tools.db_put('default_wallet', wallet_name)

    privkey = tools.det_hash(wallet['seed'])
    pubkey = tools.privtopub(privkey)

    tools.db_put('privkey', privkey)
    tools.db_put('pubkey', pubkey)

    processes = [
        {'target': tools.heart_monitor,
         'name': 'heart_monitor'},
        {'target': blockchain.main,
         'name': 'blockchain'},
        {'target': api.main,
         'name': 'api'},
        {'target': peers_check.main,
         'args': (tools.db_get('peers'),),
         'name': 'peers_check'},
        {'target': networking.serve_forever,
         'args': (peer_recieve_func, custom.port, custom.queues['heart_queue'], True),
         'name': 'peer_recieve'},
        {'target': miner.main,
         'args': (pubkey, ),
         'name': 'miner'}
    ]

    running_processes = []
    for process in processes[1:]:
        cmd = multiprocessing.Process(**process)
        cmd.start()
        running_processes.append(cmd)
        tools.log('starting ' + cmd.name)

    tools.db_put('address', tools.make_address([pubkey], 1))
    tools.log('stop: ' + str(tools.db_get('stop')))

    # until stop command puts into db, threads module will stay in this loop
    while not tools.db_get('stop'):
        time.sleep(0.5)

    # start the stopping
    custom.queues['heart_queue'].put('stop')
    for p in [[custom.port, '127.0.0.1'],
              [custom.api_port, '127.0.0.1']]:
        networking.connect('stop', p[0], p[1])
    running_processes.reverse()

    # process = psutil.Process(os.getpid())
    # for proc in process.get_children(recursive=True):
    #    print proc.pid
    #    proc.kill()

    time.sleep(2)

    for cmd in running_processes[:-1]:
        print 'im waiting for %s' % str(cmd)
        cmd.terminate()
        cmd.join()

    print('all processes stopped')
    sys.exit(0)


if __name__ == '__main__':
    try:
        print sys.argv
        main(sys.argv[1])
    except Exception as exc:
        tools.log(exc)
