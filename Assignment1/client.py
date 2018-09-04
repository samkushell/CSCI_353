import socket
import argparse

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
logfile = open(args.logfile, "w")
shouldConnect = False

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	# attempt connection
	logfile.write("connecting to the server " + args.ip + " at port " + str(args.port) + "\n")
	sock.sendto(registerMsg, server_address)
	logfile.write("sending register message " + args.name + "\n")
  	# verify connection from server
	data, server_detail = sock.recvfrom(1024)
	print data
	if (data == welcomeMsgCheck):
		logfile.write("recieved welcome\n")
		print(args.name + " connected to server and registered")
		print(args.name + " waiting for messages...")
		shouldConnect = True;
	else: 
		print "oh no!"
	while (shouldConnect):
		user_input=str(raw_input(">"))
		if (user_input == "exit"):
			shouldConnect = False;
except:
	print "Something went wrong while connecting to server"
finally:
	logfile.write("terminating client...")
	logfile.close()
	sock.close()
