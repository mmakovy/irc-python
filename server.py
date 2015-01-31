import asyncore
import zoznam
import optparse
import ConfigParser
import os
import signal
import sys
import httplib
import Queue
import threading
import chat_server
import chat_handler

q1 = Queue.Queue()

def title_thread(q1):
	data = zoznam.Zoznam()
	while True:
		item = q1.get()
		site,users = item
		conn = httplib.HTTPConnection(site)
		try:
			conn.request("GET", "/")
			response = conn.getresponse()
			source_code = response.read()
			cut = source_code.split('<title>')[1]
                	title = cut.split('</title>')[0] 
		except Exception:
			title = 'URL could not be resolved'

		if users is None:
			data.send_all(title,'server')
		else:
			data.send_to_list(users,title,'server')

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
    capacity = int(config.get("server", "capacity"))
else:
    capacity = options.capacity

def signal_handler(signal, frame):
	
	data = zoznam.Zoznam()
	data.close_all()
	server.close()
	asyncore.close_all()
	newThread.join(1)
        sys.exit(0)

if __name__ == "__main__":

	newThread = threading.Thread(target=title_thread,args=(q1,))
	newThread.daemon = True
	newThread.start()
 
	server = chat_server.ChatServer(address, port,q1)

	signal.signal(signal.SIGINT, signal_handler)
 
	print('Serving on ' + address + ':' + str(port))
	asyncore.loop()
