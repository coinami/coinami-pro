"""This file explains how we tell if a transaction is valid or not, it explains
how we update the database when new transactions are added to the blockchain."""

import copy
import custom
import tools

E_check = tools.E_check


def sigs_match(Sigs, Pubs, msg):
    pubs = copy.deepcopy(Pubs)
    sigs = copy.deepcopy(Sigs)

    def match(sig, pubs, msg):
        # for every pubkey in pubs
        for p in pubs:
            # verify is a simple verification method for signed messages
            if tools.verify(msg, sig, p):
                return {'bool': True, 'pub': p}
        return {'bool': False}

    # for every signature
    for sig in sigs:

        a = match(sig, pubs, msg)

        if not a['bool']:
            return False

        sigs.remove(sig)
        pubs.remove(a['pub'])
    return True


# This function checks if a transaction is valid and actually made by the owner of wallet.
def signature_check(tx):
    tx_copy = copy.deepcopy(tx)

    # look if signature is present in the tx
    if not E_check(tx, 'signatures', list):
        tools.log('no signautres')
        return False
    # look if pubkey is present in the tx
    if not E_check(tx, 'pubkeys', list):
        tools.log('no pubkeys')
        return False

    # We need to exclude the signatures field from tx.
    tx_copy.pop('signatures')

    # is pubkey valid?
    if len(tx['pubkeys']) == 0:
        tools.log('pubkey error')
        return False

    # if sign is longer than pubkey?
    if len(tx['signatures']) > len(tx['pubkeys']):
        tools.log('sigs too long')
        return False

    # Take det_hash of tx without signature
    msg = tools.det_hash(tx_copy)

    # check signature match between; signature field, pubkey and hashed msg 
    # sigs_match is defined at the top of this file
    if not sigs_match(copy.deepcopy(tx['signatures']),
                      copy.deepcopy(tx['pubkeys']), msg):
        tools.log('sigs do not match')
        return False

    return True


def spend_verify(tx, txs, out):
    if not E_check(tx, 'to', [str, unicode]):
        out[0] += 'No address\n'
        return False

    if not signature_check(tx):
        out[0] += 'Signature check\n'
        return False

    if len(tx['to']) <= 30:
        out[0] += 'That address is too short\n'
        return False

    if not E_check(tx, 'amount', int):
        out[0] += 'No amount\n'
        return False

    if not tools.fee_check(tx, txs):
        out[0] += 'Fee check error\n'
        return False

    if 'vote_id' in tx:
        if not tx['to'][:-29] == '11':
            out[0] += 'cannot hold votecoins in a multisig address\n'
            return False
    return True


def mint_verify(tx, txs, out):
    return 0 == len(filter(lambda t: t['type'] == 'mint', txs))


tx_check = {'spend': spend_verify,
            'mint': mint_verify}

# ------------------------------------------------------

adjust_int = tools.adjust_int
adjust_dict = tools.adjust_dict
adjust_list = tools.adjust_list
symmetric_put = tools.symmetric_put


# They most probably update the database after a transaction is made
def mint(tx, add_block):
    address = tools.addr(tx)
    adjust_int(['amount'], address, custom.block_reward, add_block)
    adjust_int(['count'], address, 1, add_block)


def spend(tx, add_block):
    address = tools.addr(tx)
    adjust_int(['amount'], address, -tx['amount'], add_block)
    adjust_int(['amount'], tx['to'], tx['amount'], add_block)
    adjust_int(['amount'], address, -custom.fee, add_block)
    adjust_int(['count'], address, 1, add_block)


update = {'mint': mint,
          'spend': spend}
