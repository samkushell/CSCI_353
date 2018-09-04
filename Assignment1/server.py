import socket
import argparse


# parse initial commands
parser = argparse.ArgumentParser(conflict_handler= "resolve")
parser.add_argument("-p", metavar = "portno", type = int, help = "the port number for the chat server", dest = "port")
parser.add_argument("-l", metavar = "logfile", help = "name of the logfile", dest = "logfile")
parser.add_argument("-h", metavar = "handler", type = int, help = "indicates how unknown clients handled", dest = "handler")
args = parser.parse_args()

# open file
logfile = open(args.logfile, "w")

# initialize socket
ip = "localhost";
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # Create a socket object
s.bind((ip, args.port))                                     # Bind to the port
logfile.write("server started on " + ip + " at port " + str(args.port) + "...\n");

# do server work
buffSize = 1024
while (True):
	# listen for new connections
	clientName = ""
	data, client_address = s.recvfrom(buffSize)
	logfile.write("client connection from host " + client_address[0] + " port " + str(client_address[1]) + "\n")
	if (data):
		splitData = data.split(" ")
		if (splitData[0] == 'register'):
			logfile.write("recieved " + data + " from host " + client_address[0] + " port " + str(client_address[1]) + "\n")
			welcomeMsg = "welcome " + splitData[1]
			s.sendto(welcomeMsg, client_address)
			print(splitData[1] + " registered from host " + client_address[0] + " port " + str(client_address[1]))
# teardown
logfile.write("terminating server...")
logfile.close()
s.close()



#TODO: FIGURE OUT HOW TO WRITE TERMINATING ON EXIT