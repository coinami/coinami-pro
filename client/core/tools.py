"""A bunch of functions that are used by multiple threads. <- Exactly
"""
import copy
import hashlib
import json
import logging
import os
import re
import subprocess
import time
import urllib2
from json import dumps as package, loads as unpackage

import AESCipher
import custom
import pt

try:
    from cdecimal import Decimal
except:
    from decimal import Decimal


# These are the functions that were added for Coinami

def edit_contact(contact, index):
    if not valid_address(contact[1]):
        return 'Address is not valid\n'

    contacts = db_get('contacts')
    del contacts[index]
    contact_json = {'name': contact[0], 'address': contact[1]}
    contacts.insert(index, contact_json)

    file_name = db_get('default_wallet')
    key = db_get('default_wallet_key')
    AESCipher.decrypt_file(key, file_name, file_name + '.dec')

    with open(file_name + '.dec') as data_file:
        my_read = data_file.read()
        data_file.close()
        os.remove(file_name + '.dec')

        try:
            data = json.loads(my_read)
        except:
            return 'Could not add contact\n'
        if 'seed' in data.keys():
            data['contacts'] = contacts
        else:
            return 'Could not add contact\n'

        data_file = open(db_get('default_wallet'), 'w')
        data_file.write(json.dumps(data))
        data_file.close()
        AESCipher.encrypt_into(key, file_name)

    db_put('contacts', contacts)
    return 'Updated contact \nName: ' + contact[0] + '\nAddress: ' + contact[1]


def remove_contact(index):
    contacts = db_get('contacts')
    temp_contact = copy.deepcopy(contacts[index])
    del contacts[index]

    file_name = db_get('default_wallet')
    key = db_get('default_wallet_key')
    AESCipher.decrypt_file(key, file_name, file_name + '.dec')

    with open(file_name + '.dec') as data_file:
        my_read = data_file.read()
        data_file.close()
        os.remove(file_name + '.dec')

        try:
            data = json.loads(my_read)
        except:
            return 'Could not add contact\n'
        if 'seed' in data.keys():
            data['contacts'] = contacts
        else:
            return 'Could not add contact\n'

        data_file = open(db_get('default_wallet'), 'w')
        data_file.write(json.dumps(data))
        data_file.close()
        AESCipher.encrypt_into(key, file_name)

    db_put('contacts', contacts)
    return 'Removed contact \nName: ' + temp_contact[0] + '\nAddress: ' + temp_contact[1]


def add_contact(contact):
    if not valid_address(contact[1]):
        return 'Address is not valid\n'

    contacts = db_get('contacts')
    contact_json = {'name': contact[0], 'address': contact[1]}
    contacts.append(contact_json)

    file_name = db_get('default_wallet')
    key = db_get('default_wallet_key')
    AESCipher.decrypt_file(key, file_name, file_name + '.dec')

    with open(file_name + '.dec') as data_file:
        my_read = data_file.read()
        data_file.close()
        os.remove(file_name + '.dec')

        try:
            data = json.loads(my_read)
        except:
            return 'Could not add contact\n'
        if 'seed' in data.keys():
            data['contacts'] = contacts
        else:
            return 'Could not add contact\n'

        data_file = open(db_get('default_wallet'), 'w')
        data_file.write(json.dumps(data))
        data_file.close()
        AESCipher.encrypt_into(key, file_name)

    db_put('contacts', contacts)
    return 'Added contact \nName: ' + contact[0] + '\nAddress: ' + contact[1]


def generate_seed():
    words = []
    f = open('core/tools/english.txt', 'r')
    for line in f:
        words.append(line.rstrip('\n'))
    import random
    mysample = random.sample(set(words), 10)
    string = ''
    for element in mysample:
        string += element + ' '
    return string


def read_wallet(file_name, key):
    wallet = {}
    wallet['valid'] = False
    file_name = os.path.join(custom.wallets_dir, str(file_name))
    try:
        open(file_name)
    except:
        wallet['message'] = 'Wallet file could not be read'
        return wallet

    if not key:
        wallet['message'] = 'You have to enter a password to open the wallet'
        return wallet

    AESCipher.decrypt_file(key, file_name, file_name + '.dec')

    with open(file_name + '.dec') as data_file:
        my_read = data_file.read()
        data_file.close()
        os.remove(file_name + '.dec')

        try:
            data = json.loads(my_read)
        except:
            wallet['message'] = 'There is a problem with encryption or wallet file is corrupted!'
            return wallet

        if 'seed' not in data:
            wallet['message'] = 'Wallet file has missing arguments(seed)!'
        else:
            wallet['valid'] = True
            wallet['seed'] = data['seed']
            if 'contacts' not in data.keys():
                wallet['contacts'] = []
            else:
                wallet['contacts'] = data['contacts']
    return wallet


def create_new_wallet(wallet_name, key, seed=None, contacts=[]):
    if seed == None:
        seed = generate_seed()

    print ":".join("{:02x}".format(ord(c)) for c in key)

    data = {}
    data['seed'] = seed
    data['contacts'] = contacts

    if not os.path.exists(custom.wallets_dir):
        os.makedirs(custom.wallets_dir)

    wallet_name = os.path.join(custom.wallets_dir, str(wallet_name))
    f = open(wallet_name, 'w')
    f.write(json.dumps(data))
    f.close()
    AESCipher.encrypt_into(key, wallet_name)
    return wallet_name


def cost_0(txs, address):
    # cost of the zeroth confirmation transactions
    total_cost = []
    votecoin_cost = {}
    # address=tools.db_get('address')
    for Tx in filter(lambda t: address == addr(t), txs):
        def spend_(total_cost=total_cost):
            total_cost.append(custom.fee)
            total_cost += [Tx['amount']]

        Do = {'spend': spend_,
              'mint': (lambda: total_cost.append(-custom.block_reward))}

        Do[Tx['type']]()
    return sum(total_cost)


def fee_check(tx, txs):
    address = addr(tx)
    cost = cost_0(txs + [tx], address)
    acc = db_get(address)
    if int(acc['amount']) < cost:
        log('insufficient money')
        return False
    return True


def get_(loc, thing):
    if loc == []: return thing
    return get_(loc[1:], thing[loc[0]])


def set_(loc, dic, val):
    get_(loc[:-1], dic)[loc[-1]] = val
    return dic


def adjust(pubkey, f):  # location shouldn't be here.
    acc = db_get(pubkey)
    f(acc)
    db_put(pubkey, acc)


def adjust_int(key, pubkey, amount, add_block):
    def f(acc, amount=amount):
        if not add_block: amount = -amount
        set_(key, acc, (get_(key, acc) + amount))

    adjust(pubkey, f)


def adjust_dict(location, pubkey, remove, dic, add_block):
    def f(acc, remove=remove, dic=dic):
        current = get_(location, acc)
        if remove != add_block:  # 'xor' and '!=' are the same.
            current = dict(dic.items() + current.items())
        else:
            try:
                current.pop(dic.keys()[0])
            except:
                log('current dic: ' + str(current) + ' ' + str(dic) + ' ' + str(location))
        set_(location, acc, current)

    adjust(pubkey, f)


def adjust_list(location, pubkey, remove, item, add_block):
    def f(acc, remove=remove, item=item):
        current = get_(location, acc)
        if remove != (add_block):  # 'xor' and '!=' are the same.
            current.append(item)
        else:
            current.remove(item)
        set_(location, acc, current)

    adjust(pubkey, f)


def symmetric_put(id_, dic, add_block):
    if add_block:
        db_put(id_, dic)
    else:
        db_delete(id_)


def update_peers(peers):
    for p in peers:
        add_peer(p)


# Peer must be a list of ip and port.
# peers_ranked is a list consists of ranked peers. Ranked peers are also lists that contains a peer information with rank number
def add_peer(peer, current_peers=0):
    if current_peers == 0:
        current_peers = db_get('peers_ranked')

    ips = map(lambda x: x[0][0], current_peers)
    ips = [str(ip) for ip in ips]

    log('add peer: ' + str(peer))
    current_peers.append([peer, 5, '0', 0])
    db_put('peers_ranked', current_peers)


def dump_out(queue):
    while not queue.empty():
        try:
            queue.get(False)
        except:
            pass


def heart_monitor():
    queue = custom.queues['heart_queue']
    beats = {}
    while True:
        time.sleep(0.5)
        t = time.time()
        for beat in beats:
            # There was no beat for 30 seconds
            if t - beats[beat] > 30:
                beats[beat] = t
                log('thread has an error: ' + str(beat))

        while not (queue.empty()):
            time.sleep(0.01)
            beat = queue.get(False)
            # log('heart monitor: ' +str(beat))
            if beat == 'stop':
                return
            if beat not in beats:
                log('adding thread: ' + str(beat))

            beats[beat] = t


logging.basicConfig(filename=custom.log_file, level=logging.INFO)


def log(junk):
    if isinstance(junk, Exception):
        logging.exception(junk)
    else:
        logging.info(str(junk))


def can_unpack(o):
    try:
        unpackage(o)
        return True
    except:
        return False


def addr(tx): return make_address(tx['pubkeys'], len(tx['signatures']))


def sign(msg, privkey): return pt.ecdsa_sign(msg, privkey)


def verify(msg, sig, pubkey): return pt.ecdsa_verify(msg, sig, pubkey)


def privtopub(privkey): return pt.privtopub(privkey)


def hash_(x): return hashlib.sha384(x).hexdigest()[0:64]


# Maybe the most important function in the whole project.
def det_hash(x):
    """Deterministically takes sha256 of dict, list, int, or string."""
    return hash_(package(x, sort_keys=True))


# No, this is not a BEP song.
# It returns the nonce inside the block and hash without the nonce
def make_half_way(block):
    a = copy.deepcopy(block)
    a.pop('auth_sign')
    a.pop('auth_pubkey')
    return {u'auth_sign': block['auth_sign'], u'auth_pubkey': block['auth_pubkey'], u'halfHash': det_hash(a)}


def base58_encode(num):
    num = int(num, 16)
    alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    base_count = len(alphabet)
    encode = ''
    if num < 0:
        return ''
    while num >= base_count:
        mod = num % base_count
        encode = alphabet[mod] + encode
        num /= base_count
    if num:
        encode = alphabet[num] + encode
    return encode


def make_address(pubkeys, n):
    """n is the number of pubkeys required to spend from this address."""
    return str(len(pubkeys)) + str(n) + base58_encode(det_hash({str(n): pubkeys}))[0:29]


def valid_address(address):
    print address, len(address)
    if address[0] == '1' and address[1] == '1' and len(address) == 31:
        return True
    return False


def buffer_(str_to_pad, size):
    return str_to_pad.rjust(size, '0')


def E_check(dic, key, type_):
    if not isinstance(type_, list): type_ = [type_]  # conver the type into list

    if len(type_) == 0: return False  # to end the recursion.

    if not key in dic: return False  # if key not in dictionary, return false

    if isinstance(type_[0], type):  # this recursion checks the other array elements in type_
        if not isinstance(dic[key], type_[0]): return E_check(dic, key, type_[1:])
    else:
        if not dic[key] == type_[0]: return E_check(dic, key, type_[1:])

    return True


def is_number(s):
    try:
        int(s)
        return True
    except:
        return False


def is_authority(brainwallet=None, pubkey=None):
    if brainwallet != None:
        privkey = det_hash(brainwallet)
        pubkey = privtopub(privkey)

    return pubkey != None and pubkey in db_get('authorities')


def kill_processes_using_ports(ports):
    popen = subprocess.Popen(['netstat', '-lpn'],
                             shell=False,
                             stdout=subprocess.PIPE)
    (data, err) = popen.communicate()
    pattern = "^tcp.*((?:{0})).* (?P<pid>[0-9]*)/.*$"
    pattern = pattern.format(')|(?:'.join(ports))
    prog = re.compile(pattern)
    for line in data.split('\n'):
        match = re.match(prog, line)
        if match:
            pid = match.group('pid')
            subprocess.Popen(['kill', '-9', pid])


def connect_to_server(address):
    response = urllib2.urlopen(address).read()
    # succesful retrieval
    json_txt = response
    print json_txt
    json_result = json.loads(json_txt)
    return json_result


def db_get(key):
    return custom.db.get(str(key))


def db_put(key, dic):
    return custom.db.set(str(key), dic)


def db_delete(key):
    return custom.db.set(str(key), 'undefined')


def db_existence(key):
    if custom.db.get(str(key)) is not None:
        return True
    else:
        return False


def count(address):
    # Returns the number of transactions that pubkey has broadcast.

    def zeroth_confirmation_txs(address, DB):
        def is_zero_conf(t):
            other_address = make_address(t['pubkeys'], len(t['signatures']))
            return address == other_address

        return len(filter(is_zero_conf, db_get('txs')))

    current = db_get(address, custom.queues)['count']
    zeroth = zeroth_confirmation_txs(address, custom.queues)
    return current + zeroth


# This is used by peer_check.
# Control function over their blocks    
def fork_check(newblocks, length, block):
    recent_hash = det_hash(block)
    their_hashes = map(lambda x: x['prevHash'] if x['length'] > 0 else 0, newblocks) + [det_hash(newblocks[-1])]
    b = (recent_hash not in their_hashes) and newblocks[0]['length'] - 1 < length < newblocks[-1]['length']
    return b
