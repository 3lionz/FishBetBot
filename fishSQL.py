import sqlite3
from fishDebug import *
class FishDatabase:
	def __init__(self, path):
		self.path = path
	
	# Checks if a user exists in the system.
	# Returns boolean true/false.
	# Usage:
	# username	-	The username to check.
	def userExists(self, username):
		exists = 0;
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("SELECT count(*) FROM users WHERE name = ?", (username,))
			exists=cur.fetchone()[0]
		except Exception as ex:
			printIfVerbose("Exception occurred checking if user existed: " + ex.args[0])
		finally:
			con.close()
			return exists
	
	# Checks if a user have already bet on A or B
	# Returns boolean true/false
	# username 	-	The username to check.
	def userHasBet(self, username):
		exists = 0;
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("SELECT ((SELECT COUNT(*) FROM   betA WHERE username = ?) + (SELECT COUNT(*) FROM   betB WHERE username = ?))", (username, username,))
			exists=cur.fetchone()[0]
		except Exception as ex:
			printIfVerbose("Exception occurred while checking if user has bet: " + ex.args[0])
		finally:
			con.close()
			return exists
			
	# Check whether a table exists.
	# tableName	- The name of the table to check for.
	def tableExists(self, tableName):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=?", (tableName,))
			exists=cur.fetchone()[0]
		except Exception as ex:
			printIfVerbose("Exception occurred while checking if table existed: " + ex.args[0])
		finally:
			con.close()
			return exists

	# Create a table
	# tableName 	- Name of the table to create.
	def createTable(self, tableName):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("CREATE TABLE {} (`username` TEXT NOT NULL UNIQUE,`bet`	INTEGER NOT NULL DEFAULT ''0'',	PRIMARY KEY(username));".format(tableName))
		except Exception as ex:
			printIfVerbose("Exception occurred while creating table '" + tableName + "': " + ex.args[0])
		finally:
			con.close
		
	# Add one to the feed counter in the database
	def addFeed(self):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute(
				"UPDATE counters SET num = num + 1 WHERE description = 'timesFed'"
			)
			con.commit()
			cur.execute("SELECT num FROM counters WHERE description = 'timesFed'")
			fedvalue = cur.fetchone()
		except Exception as ex:
			con.rollback()
			printIfVerbose("SQL ERROR!")
		finally:
			con.close
			return fedvalue
		
	# Add one to the praise counter in the database
	def addPraise(self):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute(
				"UPDATE counters SET num = num + 1 WHERE description = 'timesPraised'")
			con.commit()
			cur.execute("SELECT num FROM counters WHERE description = 'timesPraised'")
			praisevalue = cur.fetchone()

		except Exception as ex:
			printIfVerbose("Exception occurred while praising: " + ex.args[0])
			con.rollback()
		finally:
			con.close()
			return praisevalue
	
	# Return the balance/bank balance of a user.
	# Usage:
	# Username	-	The username of the balance to get.
	def balance(self, username):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("SELECT IFNULL(chips, 0), IFNULL(bank, 0) FROM users WHERE name = ?", (username,))
			balances = cur.fetchone()
		except Exception as ex:
			printIfVerbose("Exception occurred while praising: " + ex.args[0])
		finally:
			con.close()
			return balances
	
	# Add an amount of chips to the users balance
	# Usage:
	# username		-	The username of who to add chips to.
	# chips			-	The amount of chips to add.
	# Returns:
	# cur.rowcount	-	Returns 1 for success, 0 for failure
	def addChips(self, username, chips):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
				
			# If user does not exist, create empty area.
			cur.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", (username,))
			con.commit()
			cur.execute("UPDATE users SET chips = chips + ? WHERE name = ?", (chips, username,))
			con.commit()
			con.close()
		except Exception as ex:
			printIfVerbose("Exception occurred while adding chips to the balance of" + username + " : " + ex.args[0])
		finally:
			con.close()
			return cur.rowcount
	
	# Remove an amount of chips from the users balance
	# Usage:
	# username		-	The username of who to remove chips from.
	# chips			-	The amount of chips to remove.
	# Returns:
	# cur.rowcount	-	Returns 1 for success, 0 for failure
	def removeChips(self, username, chips):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cur.execute("UPDATE users SET chips = chips - ? WHERE name = ?", (chips, username,))
			con.commit()
			con.close()
		except Exception as ex:
			printIfVerbose("Exception occurred while removing chips from the balance of" + username + " : " + ex.args[0])
		finally:
			con.close()
			return cur.rowcount
	
	# Take chips from chip balance and add it to bank, as long as it is above 0
	# and the user has enough chips in their main balance.
	# Usage:
	# Username	-	The username to add bank balance to.
	# Chips		-	The amount of chips to add to bank.
	# Returns:
	# cur.rowcount	-	Returns 1 for success, 0 for failure
	def addBank(self, username, chips):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
				
			# If user does not exist, create empty area.
			cur.execute("UPDATE users SET bank = bank + ?, chips = chips - ? WHERE name = ? AND chips >= ? AND ? > 0", (chips, chips, username, chips, chips,))
			con.commit()
		except Exception as ex:
			printIfVerbose("Exception occurred while adding to bank of" + str(username) + " : " + ex.args[0])
		finally:
			con.close()
			return cur.rowcount
	
	# Place the bet into the bet<x> table
	# Usage:
	# Character		-	The table of the character being bet on
	# Username		-	The user the bet is associated with
	# ChipsToBet	-	The chips being bet on that character
	# Returns:
	# cur.rowcount	-	Returns 1 for success, 0 for failure.
	def betChar(self, character, username, chipsToBet):
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
		#vuln to sqli, but can't parametrized
			print("Character: " + character)
			print("Username: " + username)
			print("ChipsToBet: " + str(chipsToBet))
			cur.execute("INSERT INTO %s (username,bet) VALUES(?,?)" % character, (username, int(chipsToBet)))
			con.commit()
		except Exception as ex:
			printIfVerbose("Exception occurred while " + str(username) + " attempted to bet " + str(chipsToBet) + " to " + str(character) + " bet table : " + ex.args[0])
		finally:	
			con.close
			return cur.rowcount
			
	def totalCharacterBets(self, character):
		totalBet = 0
		try:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
		#vuln to sqli, but can't parametrized
			cur.execute("SELECT SUM(bet) FROM %s" % character)
			totalBet += int(cur.fetchone()[0])
		except Exception as ex:
			printIfVerbose("Exception occurred while getting total bets of character: " + str(character) + " : " + ex.args[0])
		finally:	
			return totalBet
		
	# Counts the bets of the opponents.
	# winner	- The winning character of the current betting round.
	# May need to change this... does not need a sql connection
	def countTotalOpponentBets(self, winner):
		try:
			totalBets = 0
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			if not winner == "betA":
				if self.tableExists("betA"):
					totalBets += totalCharacterBets("betA")
			if not winner == "betB":
				if self.tableExists("betB"):
					totalBets += totalCharacterBets("betB")
			if not winner == "betC":
				if self.tableExists("betC"):
					totalBets += totalCharacterBets("betC")
			if not winner == "betD":
				if self.tableExists("betD"):
					totalBets += totalCharacterBets("betD")
		except Exception as ex:
			printIfVerbose("Exception occurred while adding to bank of" + username + " : " + ex.args[0])
		finally:
			con.close()
			return totalBets