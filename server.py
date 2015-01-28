import asynchat
import asyncore
import socket
import zoznam
import optparse
import ConfigParser
import os
import signal
import sys
 
chat_room = {}

welcome = ''
 
class ChatHandler(asynchat.async_chat):
    msg_count = 0
    name = 'unamed'
    data = zoznam.Zoznam()
    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
 
        self.set_terminator('\n')
        self.buffer = []
	self.push(welcome + ' Please state your name:'	+ self.get_terminator())
 
    def collect_incoming_data(self, data):
        self.buffer.append(data)
 
    def found_terminator(self):
        msg = ''.join(self.buffer)
	if '\r' in msg:
		msg = msg[:-1]
		self.set_terminator('\r\n')

	if (self.msg_count == 0):
		self.name = msg
		self.data.new_client(msg,self) 
	else:
		if '@' in msg:
			splited = msg.split()
			users = [self.name]
			for word in splited:				
				if '@' in word:
					users.append(word[1:])
			self.data.send_to_list(users,self.name + ": " + msg + self.get_terminator(),self.name)
		else:
			print (self.name + ': ' +  msg)
			self.data.send_all(self.name + ": " + msg + self.get_terminator(),self.name)
	
	self.buffer = []
	self.msg_count = self.msg_count + 1

    def handle_close(self,info=''):
	print("Client disconnected " + self.name + info)
	self.data.send_all("Client disconected " + self.name + ' ' + info + self.get_terminator(),'server')
	if not 'duplicate' in info:
		self.data.remove(self.name)
	self.close()

		 
class ChatServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
 
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock)

option_parser = optparse.OptionParser()
option_parser.add_option('-i', '--ip', dest='address', help='IP Address')
option_parser.add_option('-p', '--port', dest='port', help='Server port', type=int)
option_parser.add_option('-c', '--capacity', dest='capacity', help='Capacity of server', type=int)
option_parser.add_option('-w', '--welcome', dest='welcome', help='Welcome message for clients')

(options, args) = option_parser.parse_args()

config = ConfigParser.SafeConfigParser()

file_exists = os.path.isfile('config.ini')
if file_exists:
	config.read("config.ini")

if options.address is None and file_exists:
    address = config.get("server", "address")
else:
    address = options.address

if options.port is None and file_exists:
    port = int(config.get("server", "port"))
else:
    port = options.port

if options.welcome is None and file_exists:
    welcome = config.get("server", "welcome")
else:
    welcome = options.welcome

if options.capacity is None and file_exists:
    capacity = config.get("server", "capacity")
else:
    capacity = options.capacity


 
server = ChatServer(address, port)

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
	#data1 = zoznam.Zoznam()
	#data1.send_all("Server is closing" + )
	server.close()
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)
 
print('Serving on ' + address + ':' + str(port))
asyncore.loop(map=chat_room)
