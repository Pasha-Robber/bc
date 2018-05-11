from Utils import Utils

import ecdsa as ec
import binascii as ba
import hashlib as hlib
import base58 as b58

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
        pubKeyHash = Utils._pubKeyHash(self.pubKey)
        versionPayload = ''.join([pubKeyHash])
        checksum = Utils._checksum(versionPayload)
        fullPayload = ''.join([versionPayload, checksum])
        address = b58.b58encode(fullPayload)
        return str(address)
