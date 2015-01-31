import asyncore
import asynchat
import socket
import threading


class Zoznam(object):
	
	data = {}
	lock = threading.Lock()

	def get_data_length(self):
		self.lock.acquire()
		length = len(self.data)
		self.lock.release()
		return length

	def remove(self,name):
		self.lock.acquire()
		if name in self.data.keys():
			del self.data[name]
		self.lock.release()

	def new_client(self,name,handler,capacity):
		self.lock.acquire()
		if name in self.data.keys():
			self.lock.release()
			handler.push("Name already exists. You will be disconected" + handler.get_terminator())		
			handler.handle_close(info = "duplicate")
		else:
			self.data[name] = handler
			self.lock.release()	
			self.send_all('New client connected under name: ' + name ,"server")

	def send_all(self,msg,sender):
		self.lock.acquire()
		for user in self.data.keys():
			if hasattr(self.data[user],'push'):
				self.send(sender,user,self.data[user],msg)
		self.lock.release()
	
	def send_to_list(self,users,msg,sender):
		self.lock.acquire()
		for user in users:
			if user in self.data.keys():		
				self.send(sender,user,self.data[user],msg)
		self.lock.release()


	def send(self,sender,reciever,reciever_handler,msg):
		if sender != reciever:
			reciever_handler.push('. ' + msg + reciever_handler.get_terminator())
		else:
			reciever_handler.push('\033[A' + '> ' + msg + reciever_handler.get_terminator())

    	def close_all(self):
        	self.send_all('Server is closing. You will be disconnected','server')
		self.lock.acquire()
        	for handler in self.data.values():
            		handler.close()
		self.lock.release()
		

