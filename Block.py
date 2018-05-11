from time import time
from hashlib import sha256
from Pow import PoW
from Utils import Utils

class Block:
    timestamp = None
    transaction = list()
    hash = None
    prevHash = None
    nonce = None

    def __init__(self, transaction, prevHash):
        self.timestamp = int(time())
        if len(self.transaction) > 0:
            self.transaction = list()
        self.transaction.insert(0,transaction)
        self.prevHash = str(prevHash)
        pow = PoW(self, 11)
        self.nonce, self.hash = pow.run()

    def addTransaction(self, tx):
        self.transaction.append(tx)

    def hashTX(self):
        txHashes = list()
        for tx in self.transaction:
            txHashes.append(tx.ID)
        return str(sha256(('').join(txHashes).encode('utf-8')).hexdigest())


    def __getstate__(self):
        return self.timestamp, self.transaction, self.hash, self.prevHash, self.nonce

    def __setstate__(self, state):
        self.timestamp, self.transaction, self.hash, self.prevHash, self.nonce = state