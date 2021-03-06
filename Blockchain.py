import pickle, redis, time
from Utils import Utils
from Db import DB
from Block import Block
from BlockIterator import BlockIterator
from Transaction import Transaction

class Blockchain:
    blocksDb = None
    tip = None

    def __init__(self):
        self.blocksDb = DB()
        if self.blocksDb.exists('l'):
            self.tip = self.blocksDb.read('l')

    def __del__(self):
        self.tip = None
        self.blocksDb = None

    def createBC(self, address):
        cbtx = Transaction()
        cbtx.newCoinbase(address)
        genesys = Block(cbtx, '')
        self.blocksDb.write(genesys.hash, genesys)
        self.blocksDb.write('l', genesys.hash)
        self.tip = genesys.hash

    def findUnsTX(self, address):
        a = False
        UTX = list()
        STXO = dict()
        bcIter = BlockIterator(self.tip, self.blocksDb)
        while True:
            block = bcIter.next()
            for tx in block.transaction:
                txID = tx.ID
                for outID in tx.outputs:
                    if txID in STXO:
                        for spenOut in STXO[txID]:
                            if int(spenOut) == int(outID):
                                a = True
                                break
                    if a:
                        a = False
                        continue
                    if tx.canUnlockOut(address, outID):
                        if tx not in UTX:
                            UTX.append(tx)
                if not tx.isCoinbase():
                    for inpID in tx.inputs:
                        if tx.canUnlockInp(address, inpID):
                            txid = tx.inputs[inpID]['txID']
                            if txid not in STXO:
                                STXO.update({txid: list()})
                            STXO[txid].append(tx.inputs[inpID]['outID'])
            if block.prevHash == '':
                break
        return UTX

    def findSpendOuts(self, address, amount):
        sOUT = list()
        outs = list()
        uTX = self.findUnsTX(address)
        acc = 0
        at = False
        for tx in uTX:
            txID = tx.ID
            for outID in tx.outputs:
                if tx.canUnlockOut(address, outID):
                    if acc <= amount:
                        acc += tx.outputs[outID]['Value']
                        outs.append(outID)
                        if acc >= amount:
                            sOUT.append({'txid':txID,  'outs':outs})
                            at = True
                            break
            if at:
                at = False
                break
        return (acc, sOUT)

    def findUTXO(self, address):
        UTXO = list()
        unsTX = self.findUnsTX(address)
        for tx in unsTX:
            for outID in tx.outputs:
                if tx.canUnlockOut(address, outID):
                    UTXO.append(tx.outputs[outID])
        return UTXO

    def addBlock(self, transaction):
        prevHash = self.blocksDb.read('l')
        block = Block(transaction, prevHash)
        self.blocksDb.write(block.hash, block)
        self.blocksDb.write('l', block.hash)
        self.tip = block.hash

    def printChain(self):
        iter = BlockIterator(self.tip, self.blocksDb)
        while 1:
            bl = iter.next()
            print('----------')
            print('Hash: ' + bl.hash)
            print('Date: ' + time.ctime(bl.timestamp))
            if bl.prevHash == '':
                break