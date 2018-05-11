import pickle as pcl

class Utils:

    @staticmethod
    def serialize(data):
        return pcl.dumps(data)
        
    @staticmethod
    def deSerialize(data):
        return pcl.loads(data)
        
    @staticmethod
    def _base58Encode( num):
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
    
    @staticmethod
    def _base58Decode( s):
        alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
        base_count = len(alphabet)
        decoded = 0
        multi = 1
        s = s[::-1]
        for char in s:
            decoded += multi * alphabet.index(char)
            multi = multi * base_count
        return decoded