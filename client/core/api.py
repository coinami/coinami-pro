"""This is the internal API. These are the words that are used to interact with a local node that you have the password to.
   Any functionality or use case will be added to this API. GUI would probably use this module.
"""
import blockchain
import copy
import custom
import networking
import sys
import tools
import psutil


def kill(proc_pid):
    try:
        process = psutil.Process(proc_pid)
        for proc in process.get_children(recursive=True):
            proc.kill()
        process.kill()
    except:
        pass


def mine_status_gui():
    return str(tools.db_get('minestatustext'))


def easy_add_transaction(tx_orig, privkey='default'):
    tx = copy.deepcopy(tx_orig)
    if privkey in ['default', 'Default']:
        if tools.db_existence('privkey'):
            privkey = tools.db_get('privkey')
        else:
            return 'No private key is known, so the tx cannot be signed. '

    pubkey = tools.privtopub(privkey)
    address = tools.make_address([pubkey], 1)

    if 'count' not in tx:
        try:
            tx['count'] = tools.count(address, {})
        except:
            tx['count'] = 1

    # add our pubkey
    if 'pubkeys' not in tx:
        tx['pubkeys'] = [pubkey]

    # this is IMPORTANT
    # when adding new transaction which is signed by us,
    # this procedure is applied. tx without signatures is signed with our privkey.
    if 'signatures' not in tx:
        tx['signatures'] = [tools.sign(tools.det_hash(tx), privkey)]
    return blockchain.add_tx(tx)


def help_(args):
    tell_about_command = {
        'help': 'type "./cli.py help <cmd>" to learn about <cmd>. type "./cli.py commands" to get a list of '
                'all commands',
        'commands': 'returns a list of the commands',
        'start': 'type "./cli.py start" to start a full node',
        'new_address': 'type "./cli.py new_address <brain>" to make a new privkey, pubkey, and address using the '
                       'brain wallet=<brain>. If you want to use this address, you need to copy/paste the pubkey '
                       'into the file custom.py',
        'DB_print': 'prints the database that is shared between threads',
        'info': 'prints the contents of an entree in the hashtable. If you want to know what the first block was: '
                'info 0, if you want to know about a particular address <addr>: info <addr>, '
                'if you want to know about yourself: info my_address',
        'my_address': 'tells you your own address',
        'spend': 'spends money, in satoshis, to an address <addr>. Example: spend 1000 11j9csj9802hc982c2h09ds',
        'blockcount': 'returns the number of blocks since the genesis block',
        'txs': 'returns a list of the zeroth confirmation transactions that are expected to be '
               'included in the next block',
        'my_balance': 'the amount of money that you own',
        'balance': 'if you want to know the balance for address <addr>, type: ./cli.py balance <addr>',
        'log': 'records the following words into the file "log.py"',
        'stop': 'This is the correct way to stop the node. If you turn off in any other way, '
                'then you are likely to corrupt your database, and you have to redownload all the blocks again.',
        'mine': 'turn the miner on/off',
        'DB': 'returns a database of information that is shared between threads',
        'pushtx': 'publishes this transaction to the blockchain, will automatically sign the transaction if necessary: '
                  './cli.py pushtx tx privkey',
        'peers': 'tells you your list of peers'
    }
    if len(args) == 0:
        return "needs 2 words. example: 'help help'"
    try:
        return tell_about_command[args[0]]
    except:
        return str(args[0]) + ' is not a word in the help documentation.'


def peers(args):
    return tools.db_get('peers_ranked')


def peers_unranked(args):
    return tools.db_get('peers')


def info(args):
    if len(args) < 1:
        return 'not enough inputs'
    if args[0] == 'my_address':
        address = tools.db_get('address')
    else:
        address = args[0]
    return tools.db_get(address)


def my_address(args):
    return tools.db_get('address')


def spend(args):
    if len(args) < 3:
        return 'Not Enough Inputs'
    return easy_add_transaction({'type': 'spend', 'amount': int(args[0]), 'to': args[1], 'description': args[2]})


def accumulate_words(l, out=''):
    if len(l) > 0:
        return accumulate_words(l[1:], out + ' ' + l[0])
    return out


def pushtx(args):
    tx = tools.unpackage(args[0].decode('base64'))
    if len(args) == 1:
        return easy_add_transaction(tx)
    privkey = tools.det_hash(args[1])
    return easy_add_transaction(tx, privkey)


def blockcount(args): return (
    tools.db_get('length'))  # this is bullshit. Why would someone use a completely different name in api


def txs(args):        return (tools.db_get('txs'))


def txs_history(args):
    txs_hist = []
    pubkey = tools.db_get('pubkey')
    address = tools.db_get('address')
    length = tools.db_get('length')
    for i in range(length + 1):
        block = tools.db_get(i)
        txs = block[u'txs']
        for tx in txs:
            if tx[u'type'] == 'spend' and (pubkey in tx[u'pubkeys'] or address == tx[u'to']):
                txs_hist.append(tx)
    print len(txs_hist)
    return txs_hist


def total_mine_value(args):
    total = 0
    pubkey = tools.db_get('pubkey')
    length = tools.db_get('length')
    for i in range(length + 1):
        block = tools.db_get(i)
        txs = block[u'txs']
        for tx in txs:
            if tx[u'type'] == 'mint' and pubkey in tx[u'pubkeys']:
                total += custom.block_reward

    return total


def total_spend_value(args):
    total = 0
    pubkey = tools.db_get('pubkey')
    length = tools.db_get('length')
    for i in range(length + 1):
        block = tools.db_get(i)
        txs = block[u'txs']
        for tx in txs:
            if tx[u'type'] == 'spend' and pubkey in tx[u'pubkeys']:
                total += tx[u'amount'] + custom.fee

    return total


def total_received_value(args):
    total = 0
    address = tools.db_get('address')
    length = tools.db_get('length')
    for i in range(length + 1):
        block = tools.db_get(i)
        txs = block[u'txs']
        for tx in txs:
            if tx[u'type'] == 'spend' and address == tx[u'to']:
                total += tx[u'amount']

    return total


def my_balance(args, address='default'):
    if address == 'default':
        address = tools.db_get('address')
    try:
        return tools.db_get(address)['amount'] - tools.cost_0(tools.db_get('txs'), address)
    except:
        return 0


def balance(args):
    if len(args) < 1:
        return 'what address do you want the balance for?'
    return my_balance(args, args[0])


def log(args): tools.log(accumulate_words(args)[1:])


def stop_(args):
    tools.db_put('stop', True)

    kill(int(tools.db_get('miner_id')))

    return 'turning off all threads'


def commands(args): return sorted(Do.keys() + ['start', 'new_wallet'])


def add_peer(args):
    ip = args[0]
    port = args[1]
    tools.add_peer([ip, port])
    return 'peer is added'


def mine(args):
    m = not (tools.db_get('mine'))

    if m:
        if custom.server_executable != '' or custom.client_executable != '':
            m = 'on'
            tools.db_put('mine', True)
            return 'Started miner.'
        else:
            m = 'off'
            tools.db_put('mine', False)
            return 'Miner is missing.'

    elif not m:
        m = 'off'
        tools.db_put('mine', False)
        kill(int(tools.db_get('miner_id')))
        return 'Stopped the miner'

    return 'miner is currently: ' + str(m)


def minestatus(args):
    m = tools.db_get('mine')
    if m:
        return 'Miner : On, Status : ' + str(tools.db_get('miner_status'))
    else:
        return 'Miner : Off, Last Update : ' + str(tools.db_get('miner_status'))


def miner_exe(args):
    return tools.db_get('miner_id', -1)


def pass_(args): return ' '


def error_(args): return error


def contacts_(args):
    string = ''
    for contact in tools.db_get('contacts'):
        string += 'Name: ' + contact[0] + ' Address: ' + contact[1] + '\n'
    return string


def pubkey_(args):
    return tools.db_get('pubkey')


def add_contact(args):
    name = args[0]
    address = args[1]
    return tools.add_contact([name, address])


def authorities_(args):
    auth_list = []
    for authority in tools.db_get('authorities'):
        auth_list.append(authority)
    return auth_list


# This is the list of commands associated with their corresponding function calls
Do = {'spend': spend, 'contacts': contacts_, 'pubkey': pubkey_, 'add_contact': add_contact, 'authorities': authorities_,
      'miner_exe': miner_exe, 'add_peer': add_peer, 'minestatus': minestatus, 'help': help_, 'blockcount': blockcount,
      'txs': txs, 'balance': balance, 'peers_unranked': peers_unranked, 'my_balance': my_balance, 'b': my_balance,
      'info': info, '': pass_, 'my_address': my_address, 'log': log, 'stop': stop_, 'commands': commands,
      'pushtx': pushtx, 'mine': mine, 'peers': peers}


# api module starts with a DB instance and heart_queue
def main():
    def responder(dic):
        # command is received with a dictionary which supposed to contain a command key
        command = dic['command']
        if command[0] in Do:
            args = command[1:]
            try:
                out = Do[command[0]](args)
            except Exception as exc:
                tools.log(exc)
                out = 'api main failure : ' + str(sys.exc_info())
        else:
            out = str(command[0]) + ' is not a command. use "./cli.py commands" to get the list of commands. ' \
                                    'use "./cli.py help help" to learn about the help tool.'
        return out

    # api starts a network client at api port with a responder function
    try:
        return networking.serve_forever(responder, custom.api_port, custom.queues['heart_queue'])
    except Exception as exc:
        tools.log('api error')
        tools.log(exc)
