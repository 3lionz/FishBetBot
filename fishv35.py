# Threads allow functions to be run simultaneously through the python shell.
# Socket to communicate with IRC
# re to use regular expressions
import thread, socket, re

# Parsing IRC messages
import IRCMsg

# Loading config
from setup import *
# Connecting and communicating with IRC
from twitchIRC import *
# User called functions
from usercommands import *
# SQL
from fishSQL import *
from game import *

#TODO:
# Getbalancestring
# leaderboard
#
# !feed/!praise/!ping can both be used at the same time
# Mod DOS by spamming !feed
# Create table when creating a new character
# Check count total opponent bets

#OLD TODO:
#Sub drip rate (http://help.twitch.tv/customer/portal/questions/6923810-how-to-get-subscribers-list)
#/housewins
#Who did I bet on again?
#Fix the more info to show AFTER stuff has been credited/banked.
#Ctrl+f "#SQLi"
#Update initialize

config = fishConfig()
connection = TwitchConnection(config.server, config.channel, config.botnick)
connection.connectIRC()
connection.joinChannel()

fishDatabase = FishDatabase(config.pathDatabase)
userCommand = User(fishDatabase, config)
gameCommand = Game(connection)
# Join a server with a name, then join a channel.
# Starts the detection of chat and reacts accordingly.
def startBot():
	while 1: 
	#ping :rajaniemi.freenode.net
		unparsedIRC = connection.getChat()
		print(unparsedIRC)
		ircMsg = userCommand.parseIRC(unparsedIRC)
		
		# Tell twitch we are still alive
		if ircMsg.command == "ping": 
			connection.ping()
			
		# Print anything we get...
		if ircMsg.message:
		
			# ---SINGLE ARGUMENT---
			# Ping the user back
			match = re.match(r'^!ping$', ircMsg.message)
			if match:
				userCommand.pingUser(connection, ircMsg)
			# Feed the fish.
			match = re.match(r'^!feed$', ircMsg.message)
			if match:
				userCommand.feed(connection)
			# Praise lionz
			match = re.match(r'^!praise$', ircMsg.message)
			if match:
				userCommand.praise(connection)
			match = re.match(r'^!getchips$', ircMsg.message)
			if match:
				userCommand.getChips(connection, ircMsg)
			match = re.match(r'^!bal$', ircMsg.message)
			match2 = re.match(r'^!balance$', ircMsg.message)
			if match or match2:
				userCommand.bal(connection, ircMsg)
			
			# ---TWO ARGUMENTS---
			#Bank
			match = re.match(r'^!bank (?P<value>\S+)$', ircMsg.message)
			if match:
				userCommand.bank(connection, ircMsg, match.group('value'))
			#BetA
			match = re.match(r'^!beta (?P<value>\S+)$', ircMsg.message)
			if match:
				print("This guy bet on a correctly")
				print(match.group('value'))
				userCommand.betA(connection, ircMsg, match.group('value'))
			#BetB
			match = re.match(r'^!betb (?P<value>\S+)$', ircMsg.message)
			if match:
				print("This guy bet on b correctly")
				print(match.group('value'))
				
# Start the bot in <x> channel.
thread.start_new_thread (startBot, ())
