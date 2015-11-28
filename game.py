class Game:
	def __init__(self, connection):
		self.betsOpen = False
		self.connection = connection
	def startBet(self):
		self.betsOpen = True
		self.connection.sendMessage(".me Bets are now OPEN!")
	def stopBet(self):
		self.betsOpen = False
		self.connection.sendMessage(".me Bets have been CLOSED!")
	def characterWon(self, character):
		print("EUGH")