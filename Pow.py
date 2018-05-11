from sys import maxsize
from hashlib import sha256

class PoW:
    block = None
    target = None
    tb = None

    def __init__(self, block, targBits):
        self.block = block
        self.tb = targBits
        self.target = 1 << 256 - int(targBits)

    def prepareData(self, nonce):
        data = list()
        data.append(self.block.PrevHash)
        data.append(self.block.hashTX())
        data.append(hex(self.block.Timestamp))
        data.append(hex(int(self.tb)))
        data.append(hex(int(nonce)))
        return ('').join(data)

    def run(self):
        hashInt = None
        hash = None
        nonce = 0
        while nonce < maxsize:
            data = self.prepareData(nonce)
            hash = str(sha256(data.encode('utf-8')).hexdigest())
            hashInt = int(hash, 16)
            if hashInt < self.target:
                break
            else:
                nonce += 1

        return (
         nonce, hash)

    def isValid(self):
        data = self.prepareData(self.block.Nonce)
        hash = str(sha256(data.encode('utf-8')).hexdigest())
        hashInt = int(hash, 16)
        if hashInt < self.target:
            return True
        else:
            return False