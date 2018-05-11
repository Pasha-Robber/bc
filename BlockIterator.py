import redis
from Utils import Utils
from Block import Block

class BlockIterator:
    currentHash = None
    db = None

    def __init__(self, curH, Db):
        self.currentHash = curH
        self.db = Db

    def next(self):
        if self.db.exists(self.currentHash):
            block = self.db.read(self.currentHash)
            self.currentHash = block.prevHash
            return block
        else:
            return None
            
