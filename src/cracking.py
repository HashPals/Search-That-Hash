from loguru import logger
from collections import namedtuple
from multiprocessing import Pool
import warnings

warnings.filterwarnings("ignore")

config = {'api_keys': None, 'hashes': [{'098f6bcd4621d373cade4e832627b4f6': {'MD2': {'John The Ripper Format': 'md2'}, 'MD5': {'Hashcat Mode': '0', 'John The Ripper Format': 'raw-md5'}, 'MD4': {'Hashcat Mode': '900', 'John The Ripper Format': 'raw-md4'}, 'Double MD5': {'Hashcat Mode': '2600'}, 'LM': {'Hashcat Mode': '3000', 'John The Ripper Format': 'lm'}, 'RIPEMD-128': {'John The Ripper Format': 'ripemd-128'}, 'Haval-128': {'John The Ripper Format': 'haval-128-4'}, 'Tiger-128': {}, 'Skein-256(128)': {}, 'Skein-512(128)': {}, 'Lotus Notes/Domino 5': {'Hashcat Mode': '8600', 'John The Ripper Format': 'lotus5'}, 'Skype': {'Hashcat Mode': '23'}, 'ZipMonster': {}, 'PrestaShop': {'Hashcat Mode': '11000'}, 'md5(md5(md5($pass)))': {'Hashcat Mode': '3500'}, 'md5(strtoupper(md5($pass)))': {'Hashcat Mode': '4300'}, 'md5(sha1($pass))': {'Hashcat Mode': '4400'}, 'md5($pass.$salt)': {'Hashcat Mode': '10'}, 'md5($salt.$pass)': {'Hashcat Mode': '20'}, 'md5(unicode($pass).$salt)': {'Hashcat Mode': '30'}, 'md5($salt.unicode($pass))': {'Hashcat Mode': '40'}, 'HMAC-MD5 (key = $pass)': {'Hashcat Mode': '50', 'John The Ripper Format': 'hmac-md5'}, 'HMAC-MD5 (key = $salt)': {'Hashcat Mode': '60', 'John The Ripper Format': 'hmac-md5'}, 'md5(md5($salt).$pass)': {'Hashcat Mode': '3610'}, 'md5($salt.md5($pass))': {'Hashcat Mode': '3710'}, 'md5($pass.md5($salt))': {'Hashcat Mode': '3720'}, 'md5($salt.$pass.$salt)': {'Hashcat Mode': '3810'}, 'md5(md5($pass).md5($salt))': {'Hashcat Mode': '3910'}, 'md5($salt.md5($salt.$pass))': {'Hashcat Mode': '4010'}, 'md5($salt.md5($pass.$salt))': {'Hashcat Mode': '4110'}, 'md5($username.0.$pass)': {'Hashcat Mode': '4210'}, 'Snefru-128': {'John The Ripper Format': 'snefru-128'}, 'NTLM': {'Hashcat Mode': '1000', 'John The Ripper Format': 'nt'}, 'Domain Cached Credentials': {'Hashcat Mode': '1100', 'John The Ripper Format': 'mscach'}, 'Domain Cached Credentials 2': {'Hashcat Mode': '2100', 'John The Ripper Format': 'mscach2'}, 'DNSSEC(NSEC3)': {'Hashcat Mode': '8300'}, 'RAdmin v2.x': {'Hashcat Mode': '9900', 'John The Ripper Format': 'radmin'}, 'Cisco Type 7': {}, 'BigCrypt': {'John The Ripper Format': 'bigcrypt'}}}], 'offline': False, 'wordlist': None, 'hashcat': False}

class Searcher:

	def __init__(self, config):
		self.searchers_offline = [hashcat(), john()]
		self.searchers_online = [hashtoolkit(), hashsorg(), LmRainbowTabels()]
		self.Hash_input = namedtuple("Hash_input", ["text", "types", "api_keys"])
		
		self.perform_search(config)
	
	def perform_search(self, config):

		results = {}
		future = []

		for hash in config["hashes"]:

			hash_ctext = next(iter(hash.keys()))
			keys = [x.lower() for x in hash[next(iter(hash.keys()))].keys()]
			supported_searchers = []
			types = []

			if config["offline"]:
				pass

			for search in self.searchers_online:
				for hashtype in keys:
					if hashtype in search.supports:
						supported_searchers.append(search)
						types.append(hashtype)

			future = self.Hash_input(hash_ctext, types, config["api_keys"])

			self.threaded_search(future, supported_searchers) 

	def threaded_search(self, future, supported_searchers):
		'''
		processes = []
		for search in supported_searchers:
			print(self.call_searcher(search, future))

		with ThreadPoolExecutor(max_workers=4) as executor:
			running_tasks = []
			for search in supported_searchers:
				running_tasks.append(executor.submit(self.call_searcher(search, future)))
		for i in running_tasks:
			# Sometimes the APIs get really funny and return nonsense
			# this is a catchall for that specific thing
			try:
				type(i.result())
			except:
				continue
		exit(0)


		pool = Pool()
		pool.map(square, range(0, 5))
		pool.close()



			#for out in as_completed(running_tasks):
			 #   print(out.result())
		print(running_tasks)
		#[r.result() for r in running_tasks]

		# from concurrent.futures import ThreadPoolExecutor
		'''
	
	def call_searcher(self, search, future):
		try:
			return search.crack(future)
		except Exception as e:
			print(e)
			print(f"Error. Searcher {type(search).__name__} is down.")
			return False

class hashtoolkit:

	supports = set(["md5", "ntlm"])
	moduels = ["cloudscraper", "requests"]
	offline = False

	def crack(self, hash):
		try:
			Scraper = cloudscraper.create_scraper()
			HTML = Scraper.get(
				f"https://hashtoolkit.com/decrypt-hash/?hash={hash}"
			).text.splitlines()
		except:
			return False  # >> Remember to log this

		for i in range(len(HTML)):
			if "/generate-hash/?text=" in HTML[i]:

				output = HTML[i].partition("?text=")[2].split('">')[0]

				if "</a></span>" in output or 'title"' in output:
					return False  # >> And this
				else:
					return output

		return False  # >> Dont think this would ever happen but log this


class hashsorg:

	supports = set(["md5", "NTLM", "SHA-1"])
	moduels = ["requests"]
	offline = False

	# How do we implment the API key?

	def crack(self, hash):
		try:
			request = requests.get(
				f"https://hashes.org/api.php?key={key}&query={hash}", timeout=5
			).text
		except:
			print("Couldn't connect")
			return False

		# Check for false positive

		if "null" in request:
			print("Hash not found")
			return False
		if "" == request:
			print("Hash seems to be a plain?")
			return False

		output = request.split('":"')[2].split('","')[0]

		# Check for Hex

		if "$HEX[" in output:
			return bytearray.fromhex(
				final_output[5 : len(final_output) - 1]
			).decode()  # Partions it so that it only contains hex and then decodes it into ASCII

		return output


class hashcat:

	supports = set(["", "", ""])
	moduels = ["subprocess"]
	offline = True

	# How do we implement the types?? (IDs) and wordlist??

	def crack(self, hash):
		for possible_type in range(len(ids)):
			command = f"hashcat64.exe -a 0 -m {ids[possible_type]} {hash} {wordlist}"  # >> Can change for better optimization etc.....
			# Hashcat64.exe for windows
			try:
				sp.check_call(
					command,
					shell="True",
					cwd="/mnt/p/Hashcat"  # << For windows, you must put the hashcat directory for it to work. Also the wordlist must be in the directory or a full path.
					# stderr=sp.STDOUT
				)
			except sp.CalledProcessError as error:
				if (
					"'hashcat' is not recognized as an internal or external command"
					in str(error)
				):
					# >> Log this (Not in PATH)
					return False
				if "./hashcat.hctune: No such file or directory" in str(error):
					# >> Also log this (Windows error)
					return False
				# Log - Couldnt crack, ID problem and/or not found in wordlist
				continue

			possible_output = str(
				sp.check_output(
					f"{command} --show", shell=True, cwd="/mnt/p/Hashcat"
				).strip()
			).replace("'", "")

			if not "No hashes loaded." in possible_output:
				return possible_output.split(":")[1]


class john:
	pass

	"""

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

	"""

class LmRainbowTabels:

	# Ok so bug for this one, it doesnt like any word longer then 7 charcters :*(

	supports = set(["lm"])
	
	def crack(self, hash):

		url = "http://rainbowtables.it64.com:80/p3.php"

		payload = f"hashe={hash}&ifik=+Submit+&forma=tak"
		headers = {

		"Origin": "http://rainbowtables.it64.com", 
		"Cookie": "PHPSESSID=; __gads=", 
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", 
		"Referer": "http://rainbowtables.it64.com/p3.php", 
		"Connection": "close", 
		"Host": "rainbowtables.it64.com", 
		"Accept-Encoding": "gzip, deflate", 
		"Cache-Control": "max-age=0", 
		"Upgrade-Insecure-Requests": "1", 
		"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
		"Content-Length": "46", 
		"Content-Type": "application/x-www-form-urlencoded"

		}

		response = requests.request("POST", url, data=payload, headers=headers).text.split('&nbsp;')

		if "CRACKED" in response[3]:
			return(response[5])

		if "Not yet in database" in response[3]:
			print("Failed")

		if "Uncrackable with this charset" in response[3]:
			print("Failed")

class md5crypt:
	# From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
	supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])

	def crack(self, hash_obj):
		for t in hash_obj.hash_type:
			res = self.search_one_type(hash_obj, t)
			if res != False:
				return res
		return False

	def search_one_type(self, hash_obj, type):
		response = requests.get(
			"https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728"
			% (hash_obj.text, t),
			timeout=3,
		).text
		if len(response) != 0:
			return response
		else:
			return False


class nitrxgen:
	# From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
	supports = set(["md5"])

	def crack(self, hash_obj):
		response = requests.get(
			"https://www.nitrxgen.net/md5db/" + hash_obj.text, verify=False, timeout=1
		).text
		if response:
			return response
		else:
			return False



Searcher(config)
# Will try and multi-thread later
