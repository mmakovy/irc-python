import asynchat
import zoznam
import server
import re
import Queue

class ChatHandler(asynchat.async_chat):
    msg_count = 0
    name = 'unamed'
    data = zoznam.Zoznam()
    q1 = Queue.Queue()

    def __init__(self, sock, q1 = None):
        asynchat.async_chat.__init__(self, sock=sock)
 
        self.set_terminator('\n')
        self.buffer = []
	self.q1 = q1
	if self.data.get_data_length() >= server.capacity:
		self.push("Server is full" + self.get_terminator())
		self.handle_close(info = "full server")
	self.push(server.welcome + ' Please state your name:'	+ self.get_terminator())
 
    def collect_incoming_data(self, data):
        self.buffer.append(data)
 
    def found_terminator(self):

        msg = ''.join(self.buffer)
	urls = re.findall('(www[.][^\s]*[.][^\s]*)', msg)
	if '\r' in msg:
		msg = msg[:-1]
		self.set_terminator('\r\n')

	if (self.msg_count == 0):
		self.name = msg
		self.data.new_client(msg,self,server.capacity) 
	else:
		if '@' in msg:
			splited = msg.split()
			users = [self.name]
			for word in splited:				
				if '@' in word:
					users.append(word[1:])
			self.data.send_to_list(users,self.name + ": " + msg ,self.name)
			if urls:
				for url in urls:
					item = (url,users)
					self.q1.put(item)
		else:
			print (self.name + ': ' +  msg)
			self.data.send_all(self.name + ": " + msg ,self.name)
			if urls:
				for url in urls:
					item = (url,None)
					self.q1.put(item)
			
	
	self.buffer = []
	self.msg_count = self.msg_count + 1

    def handle_close(self,info=''):
	print("Client disconnected " + self.name + ' ' + info)
	self.data.send_all("Client disconected " + self.name + ' ' + info ,'server')
	if not 'duplicate' in info:
		self.data.remove(self.name)
	self.close()
