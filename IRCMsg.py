class IRCMsg:
	def __init__(self, prefix, username, command, channel, message):
		self.prefix = prefix
		self.username = username
		self.command = command
		self.channel = channel
		self.message = message