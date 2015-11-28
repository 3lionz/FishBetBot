import re, fishSQL
from IRCMsg import *
from twitchIRC import *
from fishDebug import *
class User:
	def __init__(self, database, config):
		self.database = database
		self.config = config
	
	# Parses IRC commands and return an IRCMsg object
	# Usage:
	# Text	-	The text received from IRC.
	def parseIRC(self, text):
		IRCparser = re.match(r'^(:(?P<prefix>\S+) )?(?P<command>\S+)( (?!:)(?P<channel>.+?))?( :(?P<message>.+))?$', text)
		
		parsedMessage = IRCMsg(0, 0, 0, 0, 0)
		if IRCparser:
			prefix = str(IRCparser.group('prefix'))
			usernameSearch = re.search('([^!]+)', prefix)
			username = str(usernameSearch.group())
			command = str(IRCparser.group('command'))
			channel = str(IRCparser.group('channel'))
			message = str(IRCparser.group('message'))
			parsedMessage = IRCMsg(prefix, username, command, channel, message)
		return parsedMessage
	
	def IsIntAboveZero(self, i):
		try:
			if int(i) > 0:
				return True
		except ValueError:
			return False
		return False	
			
	# Feed the fish!
	# Usage: !fish
	def feed(self, connection):
		totalFeedCount = self.database.addFeed()
		if totalFeedCount != None and len(totalFeedCount) != 0:
			printIfVerbose("Successfully fed fish." )
			connection.sendMessage("The fish have been fed " + str(totalFeedCount[0]) + " times.")

	def praise(self, connection):
		totalPraiseCount = self.database.addPraise()
		if totalPraiseCount != None and len(totalPraiseCount) != 0:
			printIfVerbose("Successfully praised." )
			connection.sendMessage("3lionz has been praised " + str(totalPraiseCount[0]) + " times.")

	# Bet on A.
	# Usage: !betA <chips>
	def betA(self, connection, ircMsg, chipsToBet):
		
		# Does the user exist? If not, get outta here.
		if self.database.userExists(ircMsg.username) == 0:
			connection.sendMessage("@" + ircMsg.username + ", you have not got any chips! Use !getchips to get started.")
			return
		
		allin = False
		
		# If not an int and isn't "all", get outta here.
		if not self.IsIntAboveZero(chipsToBet):
			if chipsToBet == "all":
				allin = True
			else:
				printIfVerbose("betA received a value which was not a positive integer.")
				return
				
		#Check that the user has not already bet on someone
		if self.database.userHasBet(ircMsg.username):
			printIfVerbose(ircMsg.username + " has already bet on someone")
			connection.sendMessage("@" + ircMsg.username + ", you have already bet on someone!")
			return
			
		#Start betting!
		try:
			# ALL IN
			# If the user is banking 'all', retrieve their current chip count and use it as the chipsToBet. Return if they have no chips. 
			balance = self.database.balance(ircMsg.username)
			print("Userbalance: " + str(balance));
			print("Userbalance[0]" + str(balance[0]))
			if allin == True:
				if not self.IsIntAboveZero(int(balance[0])):
					printIfVerbose("All in bet called with a 0 or negative amount.")
					connection.sendMessage("@" + ircMsg.username + ", you must bet a minimum of 1 chip.")
				else:
					printIfVerbose("Bet all" + str(balance[0]) + " chips on a for " + ircMsg.username + ".")
					chipsToBet = int(balance[0])
								
			# BET x AMOUNT
			# Make changes, tell the user what the changes were.
				# If below 0, get outta here.
			if not self.IsIntAboveZero(chipsToBet):
				printIfVerbose("betA called with less than 1 chip.")
				connection.sendMessage("@" + ircMsg.username + ", you must bet a minimum of 1 chip.")
				return
			# If below current balance, get outta here.-
			if int(chipsToBet) > int(balance[0]):
				printIfVerbose(ircMsg.username + " bet more chips than they possessed.")
				return
			# TODO Bet that amount on a.
			# Remove chips bet from balance
			if self.database.removeChips(ircMsg.username, chipsToBet):
				printIfVerbose("Removed " + str(chipsToBet) + " from " + str(ircMsg.username) + " 's balance")
			if self.database.betChar("betA", ircMsg.username, chipsToBet):
				printIfVerbose(ircMsg.username + " bet " + str(chipsToBet) + " on A");
			
			if allin:
				connection.sendMessage("@" + ircMsg.username + " bet all " + str(balance[0]) + " chips on A. ")
			
		except Exception as ex:
			printIfVerbose("Exception occurred while betting " + chipsToBet + " chips on A for " + ircMsg.username + ": " + ex.args[0])
	
	# Ping the user.
	# Usage: !ping
	def pingUser(self, connection, ircMsg):
		connection.sendMessage("Hello " + ircMsg.username + "!")
	
	# Put the user into the system and give them their starting chips.
	# Usage: !getChips
	def getChips(self, connection, ircMsg):
		
		if self.database.userExists(ircMsg.username) == 0:
			self.database.addChips(ircMsg.username, int(self.config.startingChips))
			connection.sendMessage("@" + ircMsg.username + ", you have been given " + str(self.config.startingChips) + " starting chips!")
		else:
			connection.sendMessage("@" + ircMsg.username + ", you have already been given some starting chips.")
	
	# Get the users balance.
	# Usage: !bal OR !balance
	def bal(self, connection, ircMsg):
		if self.database.userExists(ircMsg.username) == 0:
			connection.sendMessage("@" + ircMsg.username + ", you have not got any chips! Use !getchips to get started.")
		else:
			balance = self.database.balance(ircMsg.username)
			connection.sendMessage("@" + ircMsg.username + ", " + str(balance[0]) + " chips, " + str(balance[1]) + " banked.")
	
	# Bank some of the users chips.
	# Usage: !bank <chips>
	def bank(self, connection, ircMsg, chipsToBank):
		
		# Does the user exist? If not, get outta here.
		if self.database.userExists(ircMsg.username) == 0:
			connection.sendMessage("@" + ircMsg.username + ", you have not got any chips! Use !getchips to get started.")
			return
		
		allin = False
		
		# If not an int and isn't "all", get outta here.
		if not self.IsIntAboveZero(chipsToBank):
			if chipsToBank == "all":
				allin = True
			else:
				printIfVerbose("bank received a value which was not a positive integer.")
				return
		try:
			# If the user is banking 'all', retrieve their current chip count and use it as the chipsToBank. Return if they have no chips.
			if allin == True:
				# Call sql that gets current chips and checks it's enough.
				# printIfVerbose("bank called with 'all' for empty chip count.")
				
				balance = self.database.balance(ircMsg.username)
				print balance
				if int(balance[0]) < self.config.minBankAmount:
					printIfVerbose("All in bank called with fewer than the minBankAmount.")
					connection.sendMessage("@" + ircMsg.username + ", you must bank a minimum of " + str(self.config.minBankAmount) + " chips.")
				else:
					if self.database.addBank(ircMsg.username, balance[0]):
						printIfVerbose("Banked all" + str(balance[0]) + " chips for " + ircMsg.username + ".")
						connection.sendMessage("@" + ircMsg.username + " banked all " + str(balance[0]) + " chips. ")
				
			
			
			# Make changes, tell the user what the changes were.
			if allin == False:
				# If below minimum, get outta here.
				if int(chipsToBank) < self.config.minBankAmount:
					printIfVerbose("bank called with fewer than the minBankAmount.")
					connection.sendMessage("@" + ircMsg.username + ", you must bank a minimum of " + str(self.config.minBankAmount) + " chips.")
				else:
					if self.database.addBank(ircMsg.username, chipsToBank):
						connection.sendMessage("@" + ircMsg.username + " banked " + str(chipsToBank) + " chips. ")
				
				# updateLeaderboard()
		except Exception as ex:
			printIfVerbose("Exception occurred while banking " + chipsToBank + " chips for " + ircMsg.username + ": " + ex.args[0])
	
	def totalBetGain(character):
		# Set up database connection and cursor
		con = sqlite3.connect(self.database)
		cur = con.cursor()
		winners = dict()
		cur.execute("SELECT SUM(bet) FROM {}".format(sqlite3.escapeString(tableName)))
		totalAlliesBet = int(cur.fetchone()[0])
		cur.execute("SELECT SUM(bet) FROM {}".format(sqlite3.escapeString(opponentTable)))
		totalOpponentBet = int(cur.fetchone()[0])
		for row in cur.execute("SELECT username, bet FROM {}".format(tableName)):
			xchat.prnt(row[0])
			xchat.prnt(str(row[1]))
			winners.update({row[0]:row[1]})
		for username in winners:		
			try:
				bet = winners[username]
				xchat.prnt(str(row))
				xchat.prnt(str(username))
				xchat.prnt(str(bet))
				xchat.prnt(str(totalAlliesBet))
				# get % of pot put in for their team
				potPercent = float()
				potPercent = float((float(bet) / float(totalAlliesBet)) * 100)
				
				# get total gain
				betReturn = float(bet)
				betWinnings = float(((potPercent / 100) * totalOpponentBet) * inflation)
				betTotalGain = betReturn + betWinnings
				#Guarantee bet
				if(int(bet) > 25):
					betWinnings += 20;
				else:
					guaranteedChips = int(bet) - 5
					if(guaranteedChips > 0):
						betWinnings += guaranteedChips
				if betWinnings == int(0):
					betWinnings = 1
				
				# Add the chips to the user record in the database
				cur.execute(
					"UPDATE user SET chips = IFNULL(chips, 0) + ? WHERE name = ?"
					, (betTotalGain, username,))
				xchat.command("say @" + username + " won " + str(int(betWinnings)) + "!")
			except Exception as ex:
				printIfVerbose("Exception occurred while awarding " + str(winner) + " their winning chips: " + str(ex.args[0]))
		con.commit()
		con.close()
		cleanup()	