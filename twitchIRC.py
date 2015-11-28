# Socket is used to connect to the server, re is to parse text recieved.
import socket

class TwitchConnection:
	def __init__(self, server, channel, botnick):
		# ircsock - Socket to communicate with twitch's IRC.
		self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = server
		self.channel = channel
		self.botnick = botnick
		
	# Connect to a server with a name.
	# server:	The server to connect to.
	# botnick:	The nickname to use when joining.				
	def connectIRC(self):
		self.ircsock.connect((self.server, 6667)) # Here we connect to the server using port 6667
		self.ircsock.send("USER "+ self.botnick +" "+ self.botnick +" "+ self.botnick +" :I am a betting bot for twitch made by 3lionz!\n") # user authentication
		self.ircsock.send("NICK "+ self.botnick +"\n") # here we actually assign the nick to the bot	

	def getChat(self):
		# receive data from the server
		ircmsg = self.ircsock.recv(2048) 
		
		# removing any unnecessary linebreaks.
		ircmsg = ircmsg.strip('\n\r') 
		ircmsg = ircmsg.lower()
		return ircmsg
		
	# Used to tell twitch the bot is still "alive"
	def ping(self): 
		self.ircsock.send("PONG :Pong\n")  
	 
	# This function is used to join a channel.
	def joinChannel(self): 
		self.ircsock.send("JOIN "+ self.channel +"\n")

	# Send a message to a channel.
	def sendMessage(self, message):
		self.ircsock.send("PRIVMSG "+ self.channel +" :"+ message +"\n")