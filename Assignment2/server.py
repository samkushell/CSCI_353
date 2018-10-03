import socket
import argparse
import thread
import threading
import sys
import random


class ServerThreadList:
	def __init__(self, handler, log, serverAddress, serverSocket):
		self.namesToThreads = {}
		self.addressesToThreads = {}
		self.handler = handler
		self.serverAddress = serverAddress
		self.serverSocket = serverSocket
		self.log = log
	def append(self, inServerThread):
		self.addressesToThreads[inServerThread.address] = inServerThread
		self.namesToThreads[inServerThread.name] = inServerThread

	def registerClient(self, newClientAddress, newClientName):
		self.log.write("client connection from host " + newClientAddress[0] + " port " + str(newClientAddress[1]) + "\n")
		self.log.write("recieved register " + newClientName + " from host " + newClientAddress[0] + " port " + str(newClientAddress[1]) + "\n")
		# send validation
		serverSocket.sendto("welcome " + newClientName, newClientAddress)
		# create ServerThread for client and add to list
		newClient = ServerThread(newClientName, newClientAddress, logfile, serverSocket)
		serverThreadList.append(newClient)
		newClient.start()
		print(newClientName + " registered from host " + newClientAddress[0] + " port " + str(newClientAddress[1]))
	
	def sendMessageFromAddressToTarget(self, sourceAddress, targetName, message):
		sourceThread = self.addressesToThreads[sourceAddress]
		self.log.write("sendto " + targetClient + " from " + sourceThread.name + " " + message + "\n")
		if (targetName in self.namesToThreads):
			sourceThread.targetName = targetName
			sourceThread.targetAddress = self.namesToThreads[targetName].address
			sourceThread.message = message
			sourceThread.shouldSend = True
		else:
			self.log.write(targetName + " not registered with server")
			if (self.handler == 0):
				self.log.write("\n")
			elif (self.handler == 1):
				self.log.write(", spawning " + targetName + "\n")

				spawnAddress = (self.serverAddress[0], random.randint(5001, 65534))
				newClient = SpawnedClientThread(targetName, spawnAddress, 1024)
				newClient.start()

				newClient.log.write("connecting to the server " + self.serverAddress[0] + " at port " + str(self.serverAddress[1]) + "\n")
				newClient.socket.sendto("register " + targetName, self.serverAddress)
				newClient.log.write("sending register message " + targetName + "\n")

				sourceThread.targetName = targetName
				sourceThread.targetAddress = spawnAddress
				sourceThread.message = message
				sourceThread.shouldSend = True

class ServerThread (threading.Thread):
	def __init__(self, name, address, log, serverSocket):
		threading.Thread.__init__(self)
		self.name = name
		self.address = address
		self.serverSocket = serverSocket
		self.log = log
		self.daemon = True
		self.targetName = None
		self.targetAddress = None
		self.message = None
		self.shouldSend = False
	def run(self):
		while(True):
			if (self.shouldSend):
				if (self.targetName and self.targetAddress and self.message):
					serverSocket.sendto("recvfrom " + self.name + " " + self.message, self.targetAddress)
					self.log.write("recvfrom " + self.name + " to " + self.targetName + " " + self.message + "\n")
					self.shouldSend = False


class SpawnedClientThread (threading.Thread):
	def stopListening(self):
		self.shouldRun = False
	def __init__(self, name, address, bufferLength):
		threading.Thread.__init__(self)
		self.name = name
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(address)
		self.bufferLength = bufferLength
		self.log = open("spawned_"+name+".txt", "w", 0)
		self.shouldRun = True
		self.daemon = True
	def run(self):
		while(self.shouldRun):
			try:
				data, server_detail = self.socket.recvfrom(self.bufferLength)
				if (data):
					if (data == "welcome " + self.name):
						self.log.write("recieved welcome\n")
					else:
				 		self.log.write(data + "\n")
			except KeyboardInterrupt:
				self.log.write("terminating client...")
			except:
				self.shouldRun = False

		

# parse initial commands
parser = argparse.ArgumentParser(conflict_handler = "resolve")
parser.add_argument("-p", metavar = "portno", type = int, help = "the port number for the chat server", dest = "port")
parser.add_argument("-l", metavar = "logfile", help = "name of the logfile", dest = "logfile")
parser.add_argument("-h", metavar = "handler", type = int, help = "indicates how unknown clients handled", dest = "handler")
args = parser.parse_args()
# open file
logfile = open(args.logfile, "w", 0)
# set up socket
ip = "localhost";
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
serverSocket.bind((ip, args.port))                                     # Bind to the port
logfile.write("server started on " + ip + " at port " + str(args.port) + "...\n");
# create client list
serverThreadList = ServerThreadList(args.handler, logfile, (ip, args.port), serverSocket)
# do server work
buffSize = 1024
try:
	while (True):
		data, client_address = serverSocket.recvfrom(buffSize)
		if (data):
			# divide data into parts
			splitData = data.split(" ", 2)
			instruction = splitData[0]
			targetClient = splitData[1]
			if (len(splitData) > 2 ):
				rawMessage = splitData[2]
			# parse
			if (instruction == "register"):
				serverThreadList.registerClient(client_address, targetClient)
			elif (instruction == "sendto"):
				serverThreadList.sendMessageFromAddressToTarget(client_address, targetClient, rawMessage)
# handle shutdown
except KeyboardInterrupt:
	logfile.write("terminating server...\n")
	logfile.close()
	serverSocket.close()
	sys.exit()



#TODO: FIGURE OUT HOW TO WRITE TERMINATING ON EXIT