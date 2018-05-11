from Utils import Utils
from hashlib import sha256
from random import randint

class Transaction:
    """
    input = {
        txID: str
        outID: int
        Sig: str
        PubKey
    }

    output = {
        Value: int
        PubKey: str
    }
    """
    inputs = dict()
    outputs = dict()
    ID = None
    subsidy = 10

    def __init__(self):
        self.setID()

    def newCoinbase(self, to, data=None):
        if data == None:
            print('Reward to ' + to)
        self.inputs.update({len(self.inputs):{'txID': None,'outID': -1,'Sig': data}})
        self.outputs.update({len(self.outputs):{'Value': self.subsidy,'PubKey': to}})

    def setID(self):
        self.ID = str(sha256(str(hex(randint(1, 17**2)*randint(2, 2**2))+sha256((Utils._serialize(self))).hexdigest()+hex(randint(11, 11**2)*randint(2, 2**3))).encode('utf-8')).hexdigest())

    def isCoinbase(self):
        return len(self.inputs) == 1 and self.inputs[0]['txID'] == None and self.inputs[0]['outID'] == -1

    def newUTXOTransaction(self, frm, to, amount, bc):
        amount = int(amount)
        acc, vOuts = bc.findSpendOuts(frm, amount)
        acc = int(acc)
        if len(self.inputs) != 0 and len(self.outputs) != 0:
            self.inputs = dict()
            self.outputs = dict()
        if acc < amount:
            return False
        for vOut in vOuts:
            txid = vOut['txid']
            outIDs = vOut['outs']
            for outID in outIDs:
                self.inputs.update({len(self.inputs):{'txID': txid,'outID': outID,'Sig': frm}})
        self.outputs.update({len(self.outputs):{'Value': amount,'PubKey': to}})
        if acc > amount:
            self.outputs.update({len(self.outputs):{'Value': acc-amount,'PubKey': frm}})
        return True
    
    def canUnlockOut(self, key, id):
        return self.outputs[id]['PubKey'] == key

    def canUnlockInp(self, key, id):
        return self.inputs[id]['Sig'] == key

    def usesKey(self, inKey, key):
        return Utils._pubKeyHash(inKey) == key

    def lock(self, address):
        address = Utils._base58Decode(address)
        return address[1:len(address)-4]

    def isLockedWith(self, keyLock, key):
        return keyLock == key

    def __getstate__(self):
        return self.ID, self.subsidy, self.inputs, self.outputs

    def __setstate__(self, state):
        self.ID, self.subsidy, self.inputs, self.outputs = state
