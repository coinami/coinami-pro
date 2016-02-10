"""When a peer talks to us, this is how we generate a response. This is the external API.
"""
import blockchain
import custom
import tools


def security_check(dic):
    if 'version' not in dic or dic['version'] != custom.version:
        return {'bool': False, 'error': 'version'}
    else:
        # we could add security features here.
        return {'bool': True, 'newdic': dic}


def recieve_peer(dic):
    peer = dic['peer']
    tools.add_peer(peer[0])


def blockCount(dic):
    length = tools.db_get('length')
    return {'length': length}


def rangeRequest(dic):
    ran = dic['range']
    out = []
    counter = 0
    while (len(tools.package(out)) < custom.max_download
           and ran[0] + counter <= ran[1]):
        block = tools.db_get(ran[0] + counter, custom.queues)
        if 'length' in block:
            out.append(block)
        counter += 1
    return out


def txs(dic):
    return tools.db_get('txs')


def pushtx(dic):
    custom.queues['suggested_txs'].put(dic['tx'])
    return 'success'


def pushblock(dic):
    length = tools.db_get('length')
    block = tools.db_get(length, custom.queues)
    if 'peer' in dic:
        peer = dic['peer']
    else:
        peer = False
    if 'blocks' in dic:
        for i in range(20):
            if tools.fork_check(dic['blocks'], custom.queues, length, block):
                blockchain.delete_block(custom.queues)
                length -= 1
        for block in dic['blocks']:
            custom.queues['suggested_blocks'].put([block, peer])
    else:
        custom.queues['suggested_blocks'].put([dic['block'], peer])
    return 'success'


def peers(dic):
    return tools.db_get('peers_ranked')


def main(dic):
    # tools.log(dic)
    funcs = {'recieve_peer': recieve_peer, 'blockCount': blockCount, 'rangeRequest': rangeRequest, 'txs': txs,
             'pushtx': pushtx, 'pushblock': pushblock, 'peers': peers}
    if 'type' not in dic:
        return 'oops: ' + str(dic)
    if dic['type'] not in funcs:
        return ' '.join([dic['type'], 'is not in the api'])
    check = security_check(dic)
    if not check['bool']:
        return check
    try:
        return funcs[dic['type']](check['newdic'], custom.queues)
    except Exception as exc:
        tools.log(exc)
