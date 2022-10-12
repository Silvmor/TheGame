import socket

class Client():
    def __init__(self):
        self.sock = socket.socket()
        self.authority_messages=[]
        self.authority_advance=0
        #self.sock.bind((socket.gethostname(),2301))#optional

    def connect(self,IP=None):
        if not IP:
            IP=socket.gethostname()
        #IP='10.194.38.98'
        IP='192.168.166.98'
        self.sock.connect((IP,2300))
        self.sock.setblocking(False)
        self.receiver()

    def connection_close(self,ID):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def sender(self,msg):
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send(msg[totalsent:].encode())
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent

    def receiver(self):
        chunks=[]
        while True:
            try:
                chunk = self.sock.recv(8).decode("utf-8")
            except:
                if chunks:
                    result=''.join(chunks)
                    self.authority(result)
                    chunks.clear()
                continue
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)

    def authority(self,result):
        self.authority_messages.append(result)
        self.authority_advance=1
        print('Received :',result)

