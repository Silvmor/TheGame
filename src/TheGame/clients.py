import socket


class Client:
    def __init__(self, IP=0):
        self.sock = socket.socket()
        # self.sock.bind((socket.gethostname(),2301))#optional
        self.authority_messages = []
        self.authority_advance = 0
        if not IP:
            IP = socket.gethostname()
        self.sock.connect((IP, 2300))
        self.busy = 0

    def connect(self):
        '''This function is used to connect to the server'''
        self.sock.setblocking(False)
        self.receiver()

    def connection_close(self, ID):
        '''This function is used to close the connection'''
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def sender(self, msg):
        '''This function is used to send messages to the server'''
        self.busy = 1
        print(f"Client Sent : {msg}")
        msg = msg + "$"
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        self.busy = 0

    def receiver(self):
        '''This function is used to receive messages from the server'''
        chunks = []
        while True:
            try:
                chunk = self.sock.recv(8).decode("utf-8")
            except:
                if chunks:
                    result = "".join(chunks)
                    self.authority(result)
                    chunks.clear()
                continue
            if chunk == "":
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)

    def authority(self, result):
        '''This function is used to process the messages received from the server'''
        self.authority_messages.append(result)
        self.authority_advance = 1
        print("Client Received :", result)
