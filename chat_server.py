import asyncore
import socket
import chat_handler
import Queue

class ChatServer(asyncore.dispatcher):
    q1 = Queue.Queue()

    def __init__(self, host, port, q1 = None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
	self.q1 = q1
 
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = chat_handler.ChatHandler(sock,self.q1)
