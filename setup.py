import ConfigParser, os

def getFishbotPath(filename):
	filepath = os.path.join(os.getenv('APPDATA') + '/fishbetbot/' + filename)
	return filepath
	
class fishConfig:
	config = ConfigParser.ConfigParser()
	config.read(getFishbotPath('fish.ini'))
	
	server = config.get('IRC', 'server')											# The server the bot connects to.
	botnick = config.get('IRC', 'botnick')											# The name the bot uses.
	channel = config.get('IRC', 'channel')											# The channel which we will be interacting with
	
	inflation = float(config.get('Betting', 'inflation'))							# The amount which the pot will be multiplied by as a bonus for the winners
	startingChips = int(config.get('Betting', 'startingChips'))						# Number of chips that users will start with when they use !getchips
	dripChipsIncrement = int(config.get('Betting', 'dripChipsIncrement'))			# The number of chips that regular users will be given each time /dripchips is used if they have fewer chips than the dripChipsLimit
	dripChipsIncrementSub = int(config.get('Betting', 'dripChipsIncrementSub'))		# The number of chips that subscribers will be given each time /dripchips is used if they have fewer chips than the dripChipsLimitSub
	dripChipsLimit = int(config.get('Betting', 'dripChipsLimit'))					# The number of chips at which point regular users will no longer receive chips from /dripchips
	dripChipsLimitSub = int(config.get('Betting', 'dripChipsLimitSub'))				# The number of chips at which point subscribers will no longer receive chips from /dripchips
	minBankAmount = int(config.get('Betting', 'minBankAmount'))						# The minimum number of chips that a user must bank with !bank
	aName = config.get('Betting', 'aName')											# The name of player A
	bName = config.get('Betting', 'bName')											# The name of player B
		
	pathDatabase = getFishbotPath('records.db')										# The absolute path to the user/bets database
	pathLeaderboard = getFishbotPath('leaderboard.txt')								# The absolute path to the leaderboard file
	pathBettingStatus = getFishbotPath('bettingstatus.txt')							# The absolute path to the current betting status
	
	verbose = bool(config.get('Debug', 'verbose'))									# Prints various processing messages to xchat if True

# Needs to be run once before you can start adding records to the database. Requires no parameters.
# Creates the database file if it does not already exist, and creates the table 'user' if it does not already exist
# The user table has three columns.
#	name		TEXT	Contains the user's user name. Must be unique.
#	chips		INTEGER	Contains the user's current chip count, which they use for betting or banking.
#	bank		INTEGER	Contains the user's current bank balance, which they can add to by transferring chips.
#	subscriber	INTEGER	Contains the user's subscriber status. 0 means non-subscriber, 1 means subscriber.
def initializeDB():
	try:
		con = sqlite3.connect(pathDatabase)
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS user (name TEXT PRIMARY KEY, chips INTEGER, bank INTEGER, subscriber INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS counter (description TEXT PRIMARY KEY, num INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS beta (username TEXT NOT NULL UNIQUE PRIMARY KEY, bet INTEGER NOT NULL)")
		cur.execute("CREATE TABLE IF NOT EXISTS betb (username TEXT NOT NULL UNIQUE PRIMARY KEY, bet INTEGER NOT NULL)")
		con.commit()
	except:
		printIfVerbose("Exception occurred while initializing database: " + ex.args[0])
		con.rollback()
	finally:
		con.close()
	
	printIfVerbose("DB initialized.")