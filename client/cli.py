#!/usr/bin/env python2.7

"""
    This is the client module. All node commands will be interpreted from here. Think it as CLI.
"""

from core import *


# @param f: main thread executed with brain_wallet
def daemonize(f):
    pid = os.fork()
    if pid == 0:
        f()
    # This starts the thread in child process
    else:
        sys.exit(0)


def main(c=0):
    if type(c) == int:
        p = {'command': sys.argv[1:]}
    else:
        p = {'command': c}

    if len(p['command']) == 0:
        p['command'].append(' ')

    c = p['command']
    # c is the command array following the execution of cli.py

    if c[0] == 'start':
        # start command being executed

        r = connect({'command': 'blockcount'})  # check if a node is already working
        if is_off(r):  # nothing is working

            wallet_name = ''
            if len(c) == 2:
                wallet_name = c[1]
            key = raw_input('Please enter the password for wallet: ')
            daemonize(lambda: threads.main(wallet_name=wallet_name, key=key))  # start the threads!!!
        else:
            print('Another Coinami client is already running')
    elif c[0] == 'new_wallet':

        if not c[2] or c[2] == '':
            print('Insufficient number of arguments. Please enter the wallet name')

        else:
            wallet_loc = tools.create_new_wallet(c[1], c[2])
            return ('Your new wallet is saved at ' + wallet_loc)

    elif c[0] == 'create_info':
        if len(c) > 3:
            seed = tools.generate_seed()
            privkey = tools.det_hash(seed)
            pubkey = tools.privtopub(privkey)

            authorities = []
            ip = urllib2.urlopen('http://ip.42.pl/raw').read()
            authorities.append({'pubkey': pubkey, 'ip': ip, 'port': custom.port})

            version = 1
            f = open(c[1], 'w')
            f.write(json.dumps({'version': version, 'authorities': authorities}))
            f.close()

            wallet_loc = tools.create_new_wallet(c[2], c[3], seed)

            return 'New info.json is generated. Please serve this file from a web server and share the link with your clients.\nNew Wallet is at ' + wallet_loc
        else:
            return 'Not enough arguments'
    elif c[0] == 'update_info':
        if len(c) > 3:
            try:
                seed = tools.generate_seed()
                privkey = tools.det_hash(seed)
                pubkey = tools.privtopub(privkey)

                current_info = urllib2.urlopen(custom.info_address).read()
                info = json.loads(current_info)
                info['version'] += 1
                ip = urllib2.urlopen('http://ip.42.pl/raw').read()
                info['authorities'].append({'pubkey': pubkey, 'ip': ip, 'port': custom.port})

                f = open(c[1], 'w')
                f.write(json.dumps(info))
                f.close()

                wallet_loc = tools.create_new_wallet(c[2], c[3], seed)

                return ('Updated info.json is generated and recorded into ' + c[1] + '\nNew Wallet is at ' + wallet_loc)
            except:
                return ('There was a problem while updating older info!')
        else:
            return 'Not enough arguments'
    else:
        return run_command(p)


# @param p : json object carrying the command to networking module
# this method connects to localhost api port.
def connect(p):
    peer = ['localhost', custom.api_port]
    response = networking.send_command(peer, p, 5)
    if tools.can_unpack(response):
        response = tools.unpackage(response)
    return response


def is_off(response): return type(response) == type(
        {'a': 1}) and 'error' in response  # if response is not a dictionary or there is an error in response


# all api commands are redirected to api with connect function
def run_command(p):
    response = connect(p)

    if is_off(response):
        print('Coinami client is already off. Use "start" command to turn it on.')
    return response


if __name__ == '__main__':
    print(main())
