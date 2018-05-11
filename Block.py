from time import time
from hashlib import sha256
from Pow import PoW
from Utils import Utils

class Block:
    Timestamp = None
    Transaction = list()
    Hash = None
    PrevHash = None
    Nonce = None

    def __init__(self, Transaction, PrevHash):
        self.Timestamp = int(time())
        if len(self.Transaction) > 0:
            self.Transaction = list()
        self.Transaction.insert(0,Transaction)
        self.PrevHash = str(PrevHash)
        pow = PoW(self, 11)
        self.Nonce, self.Hash = pow.run()

    def addTransaction(self, tx):
        self.Transaction.append(tx)

    def hashTX(self):
        txHashes = list()
        for tx in self.Transaction:
            txHashes.append(tx.ID)
        return str(sha256(('').join(txHashes).encode('utf-8')).hexdigest())


    def __getstate__(self):
        return self.Timestamp, self.Transaction, self.Hash, self.PrevHash, self.Nonce

    def __setstate__(self, state):
        self.Timestamp, self.Transaction, self.Hash, self.PrevHash, self.Nonce = state