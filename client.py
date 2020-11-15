import socket
import pickle

BUFFERSIZE=512

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',8080)) # friend's server ip

class Player():
    def __init__(self):
        #data=pickle.loads(s.recv(BUFFERSIZE))
        self.id=0
        pass
    def shtable(self, x):
        i=0
        for c in x:
            for r in x[i]:
                print(' '.join(r), end=' ')
            print(); i+=1
    def loop(self):
        s.send(pickle.dumps(['gettable', self.id]))
        data=pickle.loads(s.recv(BUFFERSIZE))
        self.shtable(data)

me=Player()
me.loop()