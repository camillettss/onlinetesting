import Colors as css
import socket
import pickle
import asyncore
import random, time
random.seed(time.time())

columns=4
rows=5

BUFFERSIZE=512

class Engine():
    def __init__(self):
        self.players={}
        self.outgoing={}
        self._map=[[0 for _ in range(rows)] for _ in range(columns)]
    
    def mktable(self):
        for col in range(0,columns):
            #print('')
            for row in range(0,rows):
                pos=[row,col]; done=False
                #print(pos)
                for bot in list(self.players.values()):
                    if bot.pos==pos:
                        if self.showids:
                            #print(bot.image,bot.id,end=' '); done=True
                            self._map[col][row]=[bot.image, bot.id]
                        elif self.showpos:
                            #print(bot.image,bot.pos,end=' '); done=True
                            self._map[col][row]=[bot.image, bot.pos]
                        else:
                            #print(bot.image,end=' '); done=True
                            self._map[col][row]=[bot.image]
                if not done:
                    #print('_',end=' ')
                    self._map[col][row]=['_']
        return self._map
    
class Player():
    def __init__(self):
        # connect
        pass
    def shtable(self, x):
        i=0
        for c in x:
            for r in x[i]:
                print(' '.join(r), end=' ')
            print(); i+=1

game=Engine()#; me=Player()

m=game.mktable()
#me.shtable(m)

class MainServer(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(10)
    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection address:' + addr[0] + " " + str(addr[1]))
        pid=random.randint(100,1000)
        game.outgoing.update({pid:conn})
        game.players.update({pid:Player()})
        conn.send(pickle.dumps(['success']))
        SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      updateWorld(recievedData)
    else: self.close()

def updateWorld(x):
    if x[0]=='gettable':
        game.outgoing[x[1]].send(pickle.dumps(game.mktable()))
    else:
        print('bah')

MainServer(8080)
asyncore.loop()