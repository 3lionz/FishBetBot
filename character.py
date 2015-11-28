class Character:
	def __init__(self, name, database):
		
		# We then need to set the table to this new name.
		self.name = name
		#if not database.maxReached()
		if database.tableExists("betD"):
			printIfVerbose("Max number of characters reached!")
		elif not database.tableExists("betA"):
			database.createTable("betA")
		elif not database.tableExists("betB"):
			database.createTable("betB")
		elif not database.tableExists("betC"):
			database.createTable("betC")
		# We already know betD does not exist
		elif
			database.createTable("betD")

	def characterWon(self, character):
		print("EUGH")