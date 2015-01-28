import asyncore
import asynchat
import socket
import threading


class Zoznam(object):
	
	
	_data = {}

	def write_out(self):
		print self._data

	def remove(self,name):

		if name in self._data.keys():
			del self._data[name]


	def new_client(self,name,handler):

		if name in self._data.keys():
			
			handler.push("Name already exists. You will be disconected" + handler.get_terminator())
			handler.handle_close(info = "duplicate")
		else:
			self._data[name] = handler
			self.send_all('New client connected under name: ' + name + handler.get_terminator(),"server")


	def send_all(self,msg,sender):

		for user in self._data.keys():
			if hasattr(self._data[user],'push'):
				self.send(sender,user,msg)

	
	def send_to_list(self,users,msg,sender):

		for user in users:
			if user in self._data.keys():
				self.send(sender,user,msg)


	def send(self,sender,reciever,msg):

		if sender != reciever:
			self._data[reciever].push('. ' + msg)
		else:
			self._data[reciever].push('\033[A' + '> ' + msg)


