import socket
import argparse
import thread
import threading
import sys


class ServerThreadDictionary :
	dictionary = {}
	handler = -1
	@staticmethod
	def append(self, name, serverThread):
		dictionary[name] = serverThread
	@staticmethod
	def sendMessageFromTo(socket, message, sourceName, targetName):
		if(targetName in dictionary):
			toSend = "recvfrom " + sourceName + message
			socket.sendto(toSend, dictionary[targetName].address)
			log.write( "recvfrom " + sourceName + " to  " + targetName + " \"" + message + "\"\n")
		else:
			if (handler == 0):
				return
			if (handler == 1):
				return


class ServerThread (threading.Thread):
	def __init__(self, name, address, buffSize, log, serverSocket):
		threading.Thread.__init__(self)
		self.name = name
		self.address = address
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(address)
		self.buffSize = buffSize
		self.log = log
		self.serverSocket = serverSocket
		self.daemon = True
	def run(self):
		while(True):
			data, client_address = self.socket.recvfrom(self.buffSize)
			if (data):
				splitData = data.split(" ", 2)
				if (splitData[0] == "sendto"):
					targetClientName = splitData[1]
					rawMessage = splitData[2]
					log.write("sendto " + targetClientName + " from " + self.name + " \"" + rawMessage + "\"")
					ServerThreadDictionary.sendMessageFromTo(serverSocket, rawMessage, self.name, targetClientName)

def sendDirectMessage(message, targetClientName):
	if (message):
		return

# parse initial commands
parser = argparse.ArgumentParser(conflict_handler= "resolve")
parser.add_argument("-p", metavar = "portno", type = int, help = "the port number for the chat server", dest = "port")
parser.add_argument("-l", metavar = "logfile", help = "name of the logfile", dest = "logfile")
parser.add_argument("-h", metavar = "handler", type = int, help = "indicates how unknown clients handled", dest = "handler")
args = parser.parse_args()
# open file
logfile = open(args.logfile, "w", 0)
# make client list
# initialize socket
ip = "localhost";
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
serverSocket.bind((ip, args.port))                                     # Bind to the port
logfile.write("server started on " + ip + " at port " + str(args.port) + "...\n");
# do server work
buffSize = 1024
try:
	while (True):
		# listen for new connections
		data, client_address = serverSocket.recvfrom(buffSize)
		logfile.write("client connection from host " + client_address[0] + " port " + str(client_address[1]) + "\n")
		if (data):
			splitData = data.split(" ")
			if (splitData[0] == 'register'):
				clientName = splitData[1]
				logfile.write("recieved " + data + " from host " + client_address[0] + " port " + str(client_address[1]) + "\n")
				welcomeMsg = "welcome " + clientName
				# send validation
				print "here"
				serverSocket.sendto(welcomeMsg, client_address)
				# create ServerThread for client
				newClient = ServerThread(clientName, client_address, buffSize, logfile, serverSocket)
				print(splitData[1] + " registered from host " + client_address[0] + " port " + str(client_address[1]))

# handle shutdown
except KeyboardInterrupt:
	logfile.write("terminating server...\n")
	logfile.close()
	serverSocket.close()
	sys.exit()



#TODO: FIGURE OUT HOW TO WRITE TERMINATING ON EXIT