import ecdsa as ec
import binascii as ba
import hashlib as hlib
import Utils as ut

class Wallet:
    pubKey = None
    privKey = None

    def __init__(self):
        self.pubKey, self.privKey = self._genKeys()
    
    def _genKeys(self):
        private = ec.SigningKey.generate(curve=ec.SECP256k1)
        public = ba.hexlify(private.get_verifying_key().to_string()).decode('ascii').upper()
        return public, private
    
    def getAddress(self):
        pubKeyHash = self._pubKeyHash(self.pubKey)
        versionPayload = ''.join([pubKeyHash])
        checksum = self.checksum(versionPayload)
        fullPayload = ''.join([versionPayload, checksum])
        address = self._base58Encode(fullPayload)
        return str(address)

    def _pubKeyHash(self, key):
        pubSHA = hlib.sha256(key).hexdigest()
        pub = hlib.new('ripemd160')
        pub.update(pubSHA)
        return str(pub.hexdigest())
    
    def checksum(self, data):
        return str(hlib.sha256(hlib.sha256(data).hexdigest()).hexdigest())

    
    def _base58Encode(self, num):
        alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
        base_count = len(alphabet)
        encode = ''
        if num < 0:
            return ''
        while num >= base_count:	
            mod = num % base_count
            encode = alphabet[mod] + encode
            num = num / base_count
        if num:
            encode = alphabet[num] + encode
        return encode
    
    
    def _base58Decode(self, s):
        alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
        base_count = len(alphabet)
        decoded = 0
        multi = 1
        s = s[::-1]
        for char in s:
            decoded += multi * alphabet.index(char)
            multi = multi * base_count
        return decoded