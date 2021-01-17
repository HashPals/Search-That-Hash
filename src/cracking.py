import importlib

class Modules:

	def __init__(self, modules):
		self.moduels = moduels
	
	def import_(modules):
		for moduel in modules:
			moduel = importlib.import_module(moduel)

class Searcher:

	def __init__(self, config):
		self.searchers_offline = [hashcat()]
		self.searchers_online = [hashtoolkit(),hashesorg()]
		self.Hash_input = namedtuple('Hash_input', ['text', 'types', 'api_keys'])

		self.perform_search(self, config)

	def perform_search(self, config):

		results = {}
		future = []
		
		for hash in config["hashes"]:
			supported_searchers = []
			if config["offline"]:
				for searchers in self.searchers_offline:
					pass
					

			else:
				for methods in self.searchers_online:
					pass

		for searchers in supported_searchers:
			Modules.import_(list(dict.fromkeys([item for searchers.moduels in t for item in searchers.moduels]))) # >> Gets list of all moduels needed, removes dupes and imports them

class hashtoolkit:

	supports = set(["md5","ntlm"])
	moduels = ["cloudscraper","requests"]

	def crack(self, hash):
		try:
			Scraper = cloudscraper.create_scraper()
			HTML = Scraper.get(f"https://hashtoolkit.com/decrypt-hash/?hash={hash}").text.splitlines()
		except:
			return False # >> Remember to log this
	
		for i in range(len(HTML)):
			if "/generate-hash/?text=" in HTML[i]:
	
				output = HTML[i].partition("?text=")[2].split('">')[0]
	
				if "</a></span>" in output or 'title"' in output:
					return False # >> And this
				else:
					return output
	
		return False # >> Dont think this would ever happen but log this

class hashsorg:

	supports = set(["","",""])
	moduels = ["requests"]

	# How do we implment the API key?

	def crack(self, hash):
		try:
			request = requests.get(f"https://hashes.org/api.php?key={key}&query={hash}", timeout=5).text
		except:
			print("Couldn't connect")
			return False
	
		# Check for false positive

		if "null" in request:
			print("Hash not found") ; return False
		if "" == request:
			print("Hash seems to be a plain?") ; return False
	
		output = request.split('":"')[2].split('","')[0]
	
		# Check for Hex
	
		if "$HEX[" in output:
			return(bytearray.fromhex(final_output[5 : len(final_output) - 1]).decode()) # Partions it so that it only contains hex and then decodes it into ASCII
	
		return output

class hashcat:

	supports = set(["","",""])
	moduels = ["subprocess"]

	# How do we implement the types?? (IDs) and wordlist??

	def crack(self, hash):
		for possible_type in range(len(ids)):
			command = f"hashcat64.exe -a 0 -m {ids[possible_type]} {hash} {wordlist}" # >> Can change for better optimization etc.....
			# Hashcat64.exe for windows
			try:
				sp.check_call(
					command,
					shell="True",
					cwd='/mnt/p/Hashcat' # << For windows, you must put the hashcat directory for it to work. Also the wordlist must be in the directory or a full path.
					# stderr=sp.STDOUT
				)
			except sp.CalledProcessError as error:
				if "'hashcat' is not recognized as an internal or external command" in str(error):
					# >> Log this (Not in PATH)
					return False
				if "./hashcat.hctune: No such file or directory" in str(error):
					# >> Also log this (Windows error)
					return False
				# Log - Couldnt crack, ID problem and/or not found in wordlist
				continue

			possible_output = str(
				sp.check_output(
					f"{command} --show", shell=True, cwd='/mnt/p/Hashcat'
				).strip()
			).replace("'","")

			if not "No hashes loaded." in possible_output:
				return possible_output.split(':')[1]

class john:
	pass

	'''

	supports = set(["","",""])
	moduels = ["subprocess"]

	def crack(self, hash, quiet):
	if quiet:
		john = subprocess.Popen(
			["john", hash, "--wordlist=" + wordlist], stdout=subprocess.PIPE)
		output, error = john.communicate()
		print("Jesus take the wheel! (output not supressed)")
	
	else:
		with open('/tmp/jtr_out.txt', 'w') as output:
			john = subprocess.Popen(
			("john", "--fork=4", hash, "--wordlist=" + wordlist,), stdout=output, stderr=STDOUT)
			print("Output Supressed!")
			out, error = john.communicate()

	Thanks jabbba, will do this later :P

	'''


# Will try and multi-thread later
