#!/usr/bin/env python2.7
import qdarkstyle
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui.AboutUI as AboutUI
import ui.AddContactUI as AddContactUI
import ui.AddressUI as AddressUI
import ui.BlockInfoUI as BlockInfoUI
import ui.ChooseWalletUI as ChooseWalletUI
import ui.EncryptUI as EncryptUI
import ui.InitialUI as InitialUI
import ui.MainUI as MainUI
import ui.SignVerifyUI as SignVerifyUI
from core import *

handler = None

updateUI = {}


def openBlockInfo(self):
    global InitialUI
    InitialUI.BlockInfoUI = BlockInfoUI_Class(self.text(0).split(' ')[1])
    InitialUI.BlockInfoUI.show()


def gui_read_wallet(file_name):
    global InitialUI
    key, ok = QInputDialog.getText(InitialUI, 'Open Wallet', 'Enter your password:')
    key = str(key)
    if not ok:
        wallet = {}
        wallet['message'] = 'You have to enter a password to open the wallet'
        return wallet

    return tools.read_wallet(file_name, key), key


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class MainUI_Class(QMainWindow, MainUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUI_Class, self).__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Coinami - ' + tools.db_get('default_wallet').split('/')[-1])

        self.blockcount = 0

        self.miner_on_icon = QIcon()
        self.miner_on_icon.addPixmap(QPixmap(":/mineron/miner-on.png"), QIcon.Normal, QIcon.Off)

        self.miner_off_icon = QIcon()
        self.miner_off_icon.addPixmap(QPixmap(":/mineron/miner-off.png"), QIcon.Normal, QIcon.Off)
        self.minerData = None
        self.blockchainData = None
        self.infoPageTxs = None
        self.contacts = []

        self.center()
        self.connectActions()

        self.updateUI()

    def own_blocks_count(self, pubkey, start, count):
        blocks = []
        if start == -1:
            start = tools.db_get('length')

        for i in range(start, 0, -1):
            block_from_db = tools.db_get(str(i))
            if self.minter(block_from_db[u'txs']) == pubkey:
                blocks.append(i)
            if len(blocks) > count:
                break

        return blocks

    def own_blocks_limit(self, pubkey, start, stop):
        blocks = []
        if start == -1:
            start = tools.db_get('length')

        for i in range(start, 0, -1):
            if i == stop:
                break
            block_from_db = tools.db_get(str(i))
            if self.minter(block_from_db[u'txs']) == pubkey:
                blocks.append(i)

        return blocks

    def minter(self, txs):
        for tx in txs:
            if tx['type'] == 'mint':
                return tx['pubkeys'][0]
        return ''

    def readable_time(self, mytime):
        return time.strftime("%D %H:%M", time.localtime(int(mytime)))

    def tx_value(self, txs):
        amount = 0
        for tx in txs:
            if tx['type'] == 'spend':
                amount += int(tx['amount'])
            else:
                amount += custom.block_reward
        return amount

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onMineButton(self):
        api.mine(custom.queues, None)
        self.updateMinerPage()

    def onAddContactButton(self):
        self.addContactUI = AddContactUI_Class(listener=self.updateContactsPage)
        self.addContactUI.main()

    def onRemoveContactButton(self):
        selectedItems = self.contactsTableView.selectedIndexes()
        for item in selectedItems:
            QMessageBox.about(self, tools.remove_contact(item.row()))

    def onEditContactButton(self):
        selectedItems = self.contactsTableView.selectedIndexes()
        for item in selectedItems:
            self.addContactUI = AddContactUI_Class(listener=self.updateContactsPage, updateFlag=True)
            self.addContactUI.index = item.row()
            self.addContactUI.main()

    def onSendButton(self):
        # spend 1000 toaddress
        response = api.spend(custom.queues, [str(self.sendCoinsEdit.text()), str(self.sendAddressEdit.text()),
                                             str(self.sendDescEdit.text())])
        QMessageBox.about(self, "Transaction", response)
        self.sendCoinsEdit.setText('')
        self.sendAddressEdit.setText('')
        self.sendDescEdit.setText('')

    def onAddress(self):
        self.addressUI = TextShowUI_Class('Your Address', tools.db_get('address'))
        self.addressUI.main()

    def onSeed(self):
        self.seedUI = TextShowUI_Class('Seed of your wallet', tools.db_get('seed'))
        self.seedUI.main()

    def onPubKey(self):
        self.pubkeyUI = TextShowUI_Class('Your Public Key', tools.db_get('pubkey'))
        self.pubkeyUI.main()

    def onAbout(self):
        self.aboutUI = AboutUI_Class()

    def onWebsite(self):
        import webbrowser
        webbrowser.open("http://coinami.github.io", new=1)

    def onSignVerify(self):
        self.signVerifyUI = SignVerifyUI_Class()
        self.signVerifyUI.main()

    def onEncrypt(self):
        self.encryptUI = EncryptUI_Class()
        self.encryptUI.main()

    def onLoadMoreButton(self):
        if len(self.blockchainTabBlocks) == 0:
            new_stop = 0
        else:
            new_stop = max(self.blockchainTabBlocks[-1] - 20, 0)

        new_blocks = range(self.blockchainTabBlocks[-1] - 1, new_stop, -1)
        if len(new_blocks) != 0:
            self.blockchainTabBlocks = self.blockchainTabBlocks + new_blocks

            for i in new_blocks:
                block_from_db = tools.db_get(str(i))
                a_block = QTreeWidgetItem(["Block " + str(i),
                                           str(self.readable_time(block_from_db[u'time'])),
                                           str(block_from_db[u'auth_pubkey']),
                                           str(len(block_from_db[u'txs'])),
                                           str(self.tx_value(block_from_db[u'txs'])),
                                           str(self.minter(block_from_db[u'txs']))])
                self.blockchainTree.addTopLevelItem(a_block)

        if new_stop == 0:
            self.blockchainLoadMoreButton.setEnabled(False)

    def onContactDoubleClicked(self):
        selectedItems = self.contactsTableView.selectedIndexes()
        for item in selectedItems:
            self.sendAddressEdit.setText(tools.db_get('contacts')[item.row()]['address'])
            self.tabWidget.setCurrentIndex(1)
            break

    def onMineClearButton(self):
        tools.db_put('minestatustext', '')

    def onGenomeButton(self):
        from ConfigParser import ConfigParser

        conf = ConfigParser()
        conf.read([custom.conf_file])
        genome_location = conf.get("files", "ref")
        fname = QFileDialog.getOpenFileName(self, 'Select Genome',
                                            genome_location)
        fname = str(fname)
        if fname:
            conf.set('files', 'ref', fname)
            with open(custom.conf_file, 'wb') as configfile:
                conf.write(configfile)
            tools.db_put('minestatustext', 'Reference genome set to: ' + fname + '\n' + tools.db_get('minestatustext'))

    def connectActions(self):

        """ Blockchain Tab """
        self.blockchainLoadMoreButton.clicked.connect(self.onLoadMoreButton)

        """ Miner Tab """
        self.mineButton.clicked.connect(self.onMineButton)
        self.mineClearButton.clicked.connect(self.onMineClearButton)
        self.mineGenomeButton.clicked.connect(self.onGenomeButton)

        """ Contacts Tab """
        self.addContactButton.clicked.connect(self.onAddContactButton)
        self.removeContactButton.clicked.connect(self.onRemoveContactButton)
        self.editContactButton.clicked.connect(self.onEditContactButton)
        self.contactsTableView.doubleClicked.connect(self.onContactDoubleClicked)

        """ Send Tab """
        self.sendButton.clicked.connect(self.onSendButton)

        """ Main Menu """

        self.actionQuit.triggered.connect(self.close)

        self.actionSign_Verify_Message.triggered.connect(self.onSignVerify)
        self.actionEncrpyt_Decyrpt_Message.triggered.connect(self.onEncrypt)

        self.actionAddress.triggered.connect(self.onAddress)
        self.actionSeed.triggered.connect(self.onSeed)
        self.actionPublic_Keys.triggered.connect(self.onPubKey)

        self.actionAbout.triggered.connect(self.onAbout)
        self.actionNew_Contact.triggered.connect(self.onAddContactButton)
        self.actionOfficial_Website.triggered.connect(self.onWebsite)

    def updateInfoPage(self):
        self.infoAddressText.setText(tools.db_get('address'))
        self.infoBalanceText.setText(str(api.my_balance(custom.queues, None)))
        self.infoMineText.setText(str(api.total_mine_value(custom.queues)))
        self.infoSpendText.setText(str(api.total_spend_value(custom.queues)))
        self.infoReceivedText.setText(str(api.total_received_value(custom.queues)))

        if self.infoPageTxs is None:
            self.infoPageTxs = api.txs_history(custom.queues)

            model_txs = []
            for tx in self.infoPageTxs:
                a_tx = [tools.make_address(tx[u'pubkeys'], 1), tx[u'to'], tx[u'amount'], tx[u'description']]
                model_txs.append(a_tx)

            header = ['From', 'To', 'Amount', 'Description']

            txModel = MyTableModel(model_txs, header, self)
            self.infoTxTable.setModel(txModel)
            self.infoTxTable.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

    def updateMinerPage(self):

        def statusTextUpdate(self, minerData):
            self.mineStatusEdit.setText(minerData['status'])
            if minerData['on']:
                self.mineStatusText_2.setText('Status:')
                self.mineButton.setText('Stop Miner')
                self.mineButton.setIcon(self.miner_off_icon)
            else:
                self.mineStatusText_2.setText('Last Seen:')
                self.mineButton.setText('Start Miner')
                self.mineButton.setIcon(self.miner_on_icon)

        my_pubkey = tools.db_get('pubkey')

        if self.minerData is None:
            self.minerData = {}
            self.minerData['on'] = tools.db_get('mine')
            self.minerData['status'] = api.mine_status_gui()
            self.mineTabBlocks = self.own_blocks_count(my_pubkey, -1, 20)

            statusTextUpdate(self, self.minerData)

            self.mineTree.itemDoubleClicked.connect(openBlockInfo)
            self.mineTree.clear()
            self.mineTree.setHeaderLabels(['Block', 'Time', 'Authority', 'Tx Count', 'Tx Value'])

            for i in self.mineTabBlocks:
                block_from_db = tools.db_get(str(i))
                a_block = QTreeWidgetItem(["Block " + str(i),
                                           str(self.readable_time(block_from_db[u'time'])),
                                           str(block_from_db[u'auth_pubkey']),
                                           str(len(block_from_db[u'txs'])),
                                           str(self.tx_value(block_from_db[u'txs']))])

                self.mineTree.addTopLevelItem(a_block)

        else:
            if len(self.mineTabBlocks) == 0:
                stop = -1
            else:
                stop = self.mineTabBlocks[0]

            new_blocks = self.own_blocks_limit(my_pubkey, -1, stop)
            if len(new_blocks) != 0:
                self.mineTabBlocks = new_blocks + self.mineTabBlocks
                new_blocks.reverse()

                for i in new_blocks:
                    block_from_db = tools.db_get(str(i))
                    a_block = QTreeWidgetItem(["Block " + str(i),
                                               str(self.readable_time(block_from_db[u'time'])),
                                               str(block_from_db[u'auth_pubkey']),
                                               str(len(block_from_db[u'txs'])),
                                               str(self.tx_value(block_from_db[u'txs']))])

                    self.mineTree.insertTopLevelItem(0, a_block)

            status = api.mine_status_gui()
            if self.minerData['status'] != status or self.minerData['on'] != tools.db_get('mine'):
                self.minerData['status'] = status
                self.minerData['on'] = tools.db_get('mine')
                statusTextUpdate(self, self.minerData)

    def updateSpendPage(self):
        self.sendBalanceText.setText(str(api.my_balance(custom.queues, None)))

        txs = tools.db_get('txs')
        model_txs = []
        my_pubkey = tools.db_get('pubkey')
        for tx in txs:
            if tx[u'pubkeys'][0] == my_pubkey:
                a_tx = [tx[u'to'], tx[u'amount']]
                model_txs.append(a_tx)

        header = ['To', 'Amount']

        txModel = MyTableModel(model_txs, header, self)
        self.waitingTxsTable.setModel(txModel)
        self.waitingTxsTable.horizontalHeader().setResizeMode(QHeaderView.Stretch)

    def updateContactsPage(self):
        contacts = tools.db_get('contacts')
        if self.contacts != contacts:
            table_contacts = []
            for contact in contacts:
                table_contacts.append([contact['name'], contact['address']])

            header = ['Name', 'Address']
            contactsModel = MyTableModel(table_contacts, header, self)
            self.contactsTableView.setModel(contactsModel)
            self.contactsTableView.horizontalHeader().setResizeMode(QHeaderView.Stretch)
            self.contacts = contacts

    def updateBlockPage(self):

        def isBlockchainUpdated(blockchainData):
            if blockchainData['blockcount'] != str(api.blockcount(custom.queues)):
                return True
            if blockchainData['waitingTxs'] != str(len(api.txs(custom.queues))):
                return True
            if blockchainData['numAuth'] != str(len(api.authorities_(custom.queues))):
                return True
            return False

        def statusTextUpdate(self, blockchainData):
            self.blockCountText.setText(blockchainData['blockcount'])
            self.waitingTransactionsText.setText(blockchainData['waitingTxs'])
            self.numberOfAuthoritiesText.setText(blockchainData['numAuth'])

        if self.blockchainData is None:
            self.blockchainData = {}
            self.blockchainData['blockcount'] = str(api.blockcount(custom.queues))
            self.blockchainData['waitingTxs'] = str(len(api.txs(custom.queues)))
            self.blockchainData['numAuth'] = str(len(api.authorities_(custom.queues)))
            statusTextUpdate(self, self.blockchainData)

            self.blockchainTabBlocks = range(tools.db_get('length'), max(tools.db_get('length') - 20, 0), -1)

            self.blockchainTree.header().setResizeMode(QHeaderView.Stretch)
            self.blockchainTree.itemDoubleClicked.connect(openBlockInfo)
            self.blockchainTree.clear()
            self.blockchainTree.setHeaderLabels(['Block', 'Time', 'Authority', 'Tx Count', 'Tx Value', 'Miner'])

            for i in self.blockchainTabBlocks:
                block_from_db = tools.db_get(str(i))
                a_block = QTreeWidgetItem(["Block " + str(i),
                                           str(self.readable_time(block_from_db[u'time'])),
                                           str(block_from_db[u'auth_pubkey']),
                                           str(len(block_from_db[u'txs'])),
                                           str(self.tx_value(block_from_db[u'txs'])),
                                           str(self.minter(block_from_db[u'txs']))])
                self.blockchainTree.addTopLevelItem(a_block)

        else:
            if len(self.blockchainTabBlocks) == 0:
                stop = -1
            else:
                stop = self.blockchainTabBlocks[0]

            new_blocks = range(tools.db_get('length'), stop, -1)
            if len(new_blocks) != 0:
                self.blockchainTabBlocks = new_blocks + self.blockchainTabBlocks
                new_blocks.reverse()

                for i in new_blocks:
                    block_from_db = tools.db_get(str(i))
                    a_block = QTreeWidgetItem(["Block " + str(i),
                                               str(self.readable_time(block_from_db[u'time'])),
                                               str(block_from_db[u'auth_pubkey']),
                                               str(len(block_from_db[u'txs'])),
                                               str(self.tx_value(block_from_db[u'txs'])),
                                               str(self.minter(block_from_db[u'txs']))])
                    self.blockchainTree.insertTopLevelItem(0, a_block)

            if isBlockchainUpdated(self.blockchainData):
                self.blockchainData['blockcount'] = str(api.blockcount(custom.queues))
                self.blockchainData['waitingTxs'] = str(len(api.txs(custom.queues)))
                self.blockchainData['numAuth'] = str(len(api.authorities_(custom.queues)))
                statusTextUpdate(self, self.blockchainData)

    def updateUI(self):

        """ Info Tab """
        self.updateInfoPage()

        """ Blockchain Tab """
        self.updateBlockPage()

        """ Miner Tab """
        self.updateMinerPage()

        """ Contacts Tab """
        self.updateContactsPage()

        """ Send Tab """
        self.updateSpendPage()
        QTimer.singleShot(500, self.updateUI)

    def main(self):
        self.show()

    def closeEvent(self, event):
        tools.db_put('stop', True)
        if custom.cmds:
            for p in [[custom.port, '127.0.0.1'],
                      [custom.api_port, '127.0.0.1']]:
                networking.connect('stop', p[0], p[1])
            custom.cmds.reverse()
            for cmd in custom.cmds[:-1]:
                print 'im waiting for %s' % str(cmd)
                cmd.terminate()
                cmd.join()
        print('all processes stopped')
        sys.exit(0)


class ChooseWalletUI_Class(QMainWindow, ChooseWalletUI.Ui_Form):
    def __init__(self, parent=None):
        super(ChooseWalletUI_Class, self).__init__(parent)

        self.setupUi(self)
        self.setDefaultButton()
        self.connectActions()
        self.center()
        self.statusText.hide()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def connectActions(self):
        self.pushButton.clicked.connect(self.handleButton)

    def setDefaultButton(self):
        if not tools.db_get('default_wallet'):
            self.defaultButton.hide()
        else:
            self.defaultButton.setText("Use default wallet: %s" % tools.db_get('default_wallet').split(os.sep)[-1])

    def startThreads(self):
        DB = custom.queues
        pubkey = tools.db_get('pubkey')
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

        for process in processes:
            cmd = multiprocessing.Process(**process)
            cmd.start()
            custom.cmds.append(cmd)
            tools.log('starting ' + cmd.name)

        self.mainUI = MainUI_Class()
        QTimer.singleShot(500, self.mainUI.main)
        self.hide()

    def startClientWithWallet(self, wallet_address, wallet, info, key):
        seed = str(wallet['seed'])
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
        tools.db_put('default_wallet', wallet_address)
        tools.db_put('default_wallet_key', key)
        tools.db_put('contacts', wallet['contacts'])

        privkey = tools.det_hash(wallet['seed'])
        pubkey = tools.privtopub(privkey)

        tools.db_put('address', tools.make_address([pubkey], 1))
        tools.db_put('privkey', privkey)
        tools.db_put('pubkey', pubkey)

        QTimer.singleShot(500, self.startThreads)

    def openDefaultWallet(self):
        fname = tools.db_get('default_wallet')
        key = tools.db_get('default_wallet_key')
        print "key : ", key
        if fname:
            wallet = tools.read_wallet(fname, key)
            if not wallet['valid']:
                self.statusText.show()
                self.statusText.setText(wallet['message'])
            else:
                try:
                    info = json.loads(urllib2.urlopen(custom.info_address).read())
                except:
                    self.statusText.show()
                    self.statusText.setText(wallet['message'])
                    return
                self.statusText.show()
                self.statusText.setText('Valid wallet. Client is about to start..')
                self.startClientWithWallet(fname, wallet, info, key)

    def openSelectWallet(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            directory)
        if fname:
            fname = str(fname)
            wallet, key = gui_read_wallet(fname)
            if not wallet['valid']:
                self.statusText.show()
                self.statusText.setText(wallet['message'])
            else:
                try:
                    info = json.loads(urllib2.urlopen(custom.info_address).read())
                except:
                    self.statusText.show()
                    self.statusText.setText('No connection')
                    return
                self.statusText.show()
                self.statusText.setText('Valid wallet. Client is about to start..')
                self.startClientWithWallet(fname, wallet, info, key)

    def openNewWallet(self):
        text, ok = QInputDialog.getText(self, 'New Wallet', 'Enter your wallet name:')
        if ok:
            key, ok2 = QInputDialog.getText(self, 'Password', 'Provide a password to protect your wallet:')
            key = str(key)
            if ok2:
                wallet_location = tools.create_new_wallet(text, key)
                self.statusText.show()
                self.statusText.setText('New wallet is generated!')
                try:
                    info = json.loads(urllib2.urlopen(custom.info_address).read())
                except:
                    self.statusText.show()
                    self.statusText.setText('No connection')
                    return

                self.startClientWithWallet(wallet_location, tools.read_wallet(wallet_location, key), info, key)

    def handleButton(self):
        if self.defaultButton.isChecked():
            self.openDefaultWallet()
        elif self.selectButton.isChecked():
            self.openSelectWallet()
        elif self.newButton.isChecked():
            self.openNewWallet()
        else:
            QMessageBox.about(self, 'Warning',
                              "Please choose one option")

    def main(self):
        self.show()

    def closeEvent(self, event):
        tools.db_put('stop', True)
        if custom.processes:
            networking.connect('stop', custom.database_port, '127.0.0.1')
            custom.processes[0].join()
        if custom.cmds:
            for p in [[custom.port, '127.0.0.1'],
                      [custom.api_port, '127.0.0.1']]:
                networking.connect('stop', p[0], p[1])
            custom.cmds.reverse()
            for cmd in custom.cmds[:-1]:
                print 'im waiting for %s' % str(cmd)
                cmd.terminate()
                cmd.join()
        print('all processes stopped')
        sys.exit(0)


class InitialUI_Class(QMainWindow, InitialUI.Ui_Dialog):
    def __init__(self, parent=None):
        super(InitialUI_Class, self).__init__(parent)

        self.setupUi(self)
        self.center()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startCoinami(self):
        self.situationText.setText('Starting Coinami!')
        self.chooseWallet = ChooseWalletUI_Class()
        QTimer.singleShot(500, self.chooseWallet.main)
        self.hide()

    def connectAuthority(self):

        self.situationText.setText('Connecting to Authority!')

        try:
            info = json.loads(urllib2.urlopen(custom.info_address).read())
            self.situationText.setText('Connection Established!')
            self.can_start = True
        except:
            self.situationText.setText('Connection Failed!')
            self.can_start = False

        if self.can_start:
            QTimer.singleShot(500, self.startCoinami)

    def initializeDatabase(self):
        try:
            self.situationText.setText('Initializing Database!')
            tools.db_put('length', -1)
            print custom.db.get('length')
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
            self.close_database = False
        except:
            self.situationText.setText('Initializing Failed!')
            self.close_database = True

            return

        if self.close_database:
            self.closeDatabase()
        else:
            QTimer.singleShot(500, self.connectAuthority)

    def startDatabase(self):
        tools.log('custom.current_loc: ' + str(custom.current_loc))

        if custom.db is not None:
            self.situationText.setText('Database Started!')
            self.close_database = False
        else:
            self.situationText.setText('Database Failed!')
            self.close_database = False
            return

        b = tools.db_existence('length')

        tools.db_put('stop', False)
        tools.db_put('minestatustext', '')
        # Initialize the db
        if not b:
            QTimer.singleShot(500, self.initializeDatabase)
        else:
            QTimer.singleShot(500, self.connectAuthority)

    def initialize(self):
        self.situationText.setText('Starting Database')

        QTimer.singleShot(500, self.startDatabase)

    def main(self):
        self.show()
        self.initialize()

    def closeEvent(self, event):
        tools.db_put('stop', True)
        if custom.processes:
            networking.connect('stop', custom.database_port, '127.0.0.1')
            custom.processes[0].join()
        if custom.cmds:
            for p in [[custom.port, '127.0.0.1'],
                      [custom.api_port, '127.0.0.1']]:
                networking.connect('stop', p[0], p[1])
            custom.cmds.reverse()
            for cmd in custom.cmds[:-1]:
                print 'im waiting for %s' % str(cmd)
                cmd.terminate()
                cmd.join()
        print('all processes stopped')


class BlockInfoUI_Class(QDialog, BlockInfoUI.Ui_Dialog):
    def minter(self, txs):
        for tx in txs:
            if tx['type'] == 'mint':
                return tx['pubkeys'][0]
        return ''

    def __init__(self, blocknumber, parent=None):
        super(BlockInfoUI_Class, self).__init__(parent)

        self.setupUi(self)
        self.center()

        block = tools.db_get(str(blocknumber))
        self.blocknumberText.setText(str(blocknumber))
        self.blocknumberText.setWordWrap(True)
        self.minerText.setText(self.minter(block[u'txs']))
        self.timeText.setText(time.strftime("%D %H:%M", time.localtime(int(block[u'time']))))
        self.minerText.setWordWrap(True)
        self.authText.setText(block[u'auth_pubkey'])

        model_txs = []
        for tx in block[u'txs']:
            if tx[u'type'] == 'spend':
                a_tx = [tools.make_address(tx[u'pubkeys'], 1), tx[u'to'], tx[u'amount'], tx[u'description']]
                model_txs.append(a_tx)

        header = ['From', 'To', 'Amount', 'Description']

        txModel = MyTableModel(model_txs, header, self)
        self.txTable.setModel(txModel)
        self.txTable.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main(self):
        self.show()


class TextShowUI_Class(QDialog, AddressUI.Ui_Dialog):
    def __init__(self, title, text, parent=None):
        super(TextShowUI_Class, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.textEdit.setText(text)
        self.setWindowTitle(title)
        self.okButton.clicked.connect(self.close)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main(self):
        self.show()


class SignVerifyUI_Class(QDialog, SignVerifyUI.Ui_Dialog):
    def onSign(self):
        address = str(self.addressEdit.text())
        message = str(self.messageEdit.toPlainText())

        if tools.valid_address(address):
            signature = tools.sign(tools.det_hash({'message': message, 'address': address}), tools.db_get('privkey'))
            self.signatureEdit.setText(signature)
            return signature
        else:
            QMessageBox.error(self, 'Address', 'Address is not valid')
            return ''

    def onVerify(self):
        address = str(self.addressEdit.text())
        message = str(self.messageEdit.toPlainText())
        signature = str(self.signatureEdit.toPlainText())

        if not tools.valid_address(address):
            QMessageBox.error(self, 'Address', 'Address is not valid')
            return False
        elif signature != str(
                tools.sign(tools.det_hash({'message': message, 'address': address}), tools.db_get('privkey'))):

            QMessageBox.error(self, 'Error', 'Verification is failed')
            return False
        else:
            QMessageBox.information(self, 'Verified', 'Signature is correct')
            return True

    def __init__(self, address='', parent=None):
        super(SignVerifyUI_Class, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.address = address

        self.closeButton.clicked.connect(self.close)
        self.signButton.clicked.connect(self.onSign)
        self.verifyButton.clicked.connect(self.onVerify)

        self.addressEdit.setText(self.address)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main(self):
        self.show()


class EncryptUI_Class(QDialog, EncryptUI.Ui_Dialog):
    def onEnc(self):

        key = str(self.keyEdit.text())
        message = str(self.norEdit.toPlainText())

        mycipher = AESCipher.AESCipher_Class(key)

        encrypted = mycipher.encrypt(message)
        self.encEdit.setText(encrypted)
        return True

    def onDec(self):

        key = str(self.keyEdit.text())
        message = str(self.norEdit.toPlainText())
        encrypted = str(self.encEdit.toPlainText())

        mycipher = AESCipher.AESCipher_Class(key)
        try:
            solution = mycipher.decrypt(encrypted)
        except:
            QMessageBox.warning(self, 'Wrong', 'There is a problem with encryption!')

        self.norEdit.setText()
        return True

    def __init__(self, key='', parent=None):
        super(EncryptUI_Class, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.key = key

        self.closeButton.clicked.connect(self.close)
        self.encButton.clicked.connect(self.onEnc)
        self.decButton.clicked.connect(self.onDec)

        self.keyEdit.setText(self.key)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main(self):
        self.show()


class AddContactUI_Class(QDialog, AddContactUI.Ui_Dialog):
    def __init__(self, parent=None, listener=None, updateFlag=None):
        super(AddContactUI_Class, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.listener = listener
        self.updateFlag = updateFlag
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.okButton)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

    def okButton(self):
        if self.updateFlag is not None and self.updateFlag:
            response = tools.edit_contact([str(self.addContactNameEdit.text()), str(self.addContactAddressEdit.text())],
                                          self.index)
        else:
            response = api.add_contact(custom.queues,
                                       [str(self.addContactNameEdit.text()), str(self.addContactAddressEdit.text())])

        QMessageBox.about(self, 'Update', response)
        self.listener()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main(self):
        self.show()
        if self.updateFlag:
            self.addContactNameEdit.setText(tools.db_get('contacts')[self.index]['name'])
            self.addContactAddressEdit.setText(tools.db_get('contacts')[self.index]['address'])


class AboutUI_Class(QDialog, AboutUI.Ui_Dialog):
    def __init__(self, parent=None, listener=None):
        super(AboutUI_Class, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ErrorUI_Class(QWidget):
    def __init__(self):
        super(ErrorUI_Class, self).__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 250, 150)

        QMessageBox.about(self, 'Error',
                          "There is already a runnning Coinami Client")

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

    r = connect({'command': 'blockcount'})  # check if a node is already working
    if is_off(r):  # nothing is working

        InitialUI = InitialUI_Class()
        InitialUI.main()

        # Start opening screen
    else:
        errorUi = ErrorUI_Class()
        # Show error dialog
    sys.exit(app.exec_())
