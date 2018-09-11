import socket
import argparse
import threading
import thread
import sys

## TODO: can't quit, hung up on recvfrom?

class MessageListenerThread (threading.Thread):
	def stopListening(self):
		self.shouldRun = False
	def __init__(self, name, socket, bufferLength, log):
		threading.Thread.__init__(self)
		self.name = name
		self.socket = socket
		self.bufferLength = bufferLength
		self.log = log
		self.shouldRun = True
		self.daemon = True
	def run(self):
		print(self.name + "# waiting for messages...")
		while(self.shouldRun):
			try:
				data, server_detail = self.socket.recvfrom(self.bufferLength)
				if (data):
				 	print (self.name + "# " + data)
				 	self.log.write(data + "\n")
			except:
				self.shouldRun = False


parser = argparse.ArgumentParser(conflict_handler= "resolve")
parser.add_argument("-s", metavar = "<serverIP>",type = str, help = "indicates the server IP address", dest = "ip")
parser.add_argument("-p", metavar = "<portno>", type = int, help = "port number for client to connect to server", dest = "port")
parser.add_argument("-l", metavar = "<logfile>", type = str, help = "name of the logfile", dest = "logfile")
parser.add_argument("-n", metavar = "<myname>", type = str, help = "indicates client name", dest = "name")
args = parser.parse_args()


# useful values
server_address = (args.ip, args.port)
registerMsg = "register " + args.name
welcomeMsgCheck = "welcome " + args.name
logfile = open(args.logfile, "w", 0)
shouldConnect = False

# create socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# create thread to listen to server
listener = MessageListenerThread(args.name, clientSocket, 1024, logfile)
try:
	# attempt connection
	logfile.write("connecting to the server " + args.ip + " at port " + str(args.port) + "\n")
	clientSocket.sendto(registerMsg, server_address)
	logfile.write("sending register message " + args.name + "\n")
  	# verify connection from server
	data, server_detail = clientSocket.recvfrom(1024)
	if (data == welcomeMsgCheck):
		logfile.write("recieved welcome\n")
		#clientSocket.bind(server_address)
		print(args.name + "# connected to server and registered")
		shouldConnect = True;
		listener.start()
		while (shouldConnect):
			user_input = str(raw_input(args.name + "# "))
			if (user_input == "exit"):
				shouldConnect = False;
			elif(user_input):
				clientSocket.sendTo(user_input, server_address)
				log.write(user_input)
except:
	print "Something went wrong while connecting to server"
finally:
	logfile.write("terminating client...\n")
	logfile.close()
	listener.stopListening()
	sys.exit()
