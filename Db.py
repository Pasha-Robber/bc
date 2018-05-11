from Utils import Utils
import pickle as pkl

class DB:

    def write(self, file, value):
        with open('bc/{}'.format(file), 'wb') as f:
            pkl.dump(value, f)

    def read(self, file):
        if self.exists(file):
            with open('bc/{}'.format(file), 'rb') as f:
                data = pkl.load(f)
            return data
        else:
            return None

    def exists(self, file):
        fl = None
        try:
            fl = open('bc/{}'.format(file), 'rb')
        except FileNotFoundError:
            return False
        else:
            fl.close()
            return True
