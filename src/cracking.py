import warnings as logger
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
import requests
import cloudscraper
from rich.console import Console

console = Console()
logger.filterwarnings("ignore")

# This is an example input

# TODO :
# Get logru warnings
#


class Searcher:
    def __init__(self, config):
        self.searchers_offline = [hashcat()]  # Temp disabled until I get the IDs format
        self.searchers_online = [
            hashsorg(),
            LmRainbowTabels(),
            nitrxgen(),
        ]  # md5cryp() takes ~ 3 seconds to do
        self.Hash_input = namedtuple(
            "Hash_input", ["text", "types", "hashcats", "api_keys", "timeout"]
        )

        self.perform_search(config)

    def perform_search(self, config):
        
        if not config["timeout"]:
            config["timeout"] = 1
        #print(config["timeout"])    
        
        for hash, types in config["hashes"].items():
            hash_ctext = hash

            keys = [type["name"].lower() for type in types]
            hashcats = [type["hashcat"] for type in types]

            supported_searchers = []
            types = []

            if not config["offline"]:
                for search in self.searchers_online:
                    for hashtype in keys:
                        if hashtype.lower() in search.supports:
                            supported_searchers.append(search)
                            types.append(hashtype)
                            break

            for search in self.searchers_offline:
                for hashtype in keys:
                    if hashtype.lower() in search.supports:
                        supported_searchers.append(search)
                        types.append(hashtype)
                        break

            future = self.Hash_input(
                hash_ctext, types, hashcats, config["api_keys"], config["timeout"]
            )

            #print(future, supported_searchers) ; exit(0) 
            
            results = self.threaded_search(future, supported_searchers)
            
            for k, v in results.items():
                console.print(f"[bold blue] {k} : [bold red] {v}")

    def threaded_search(self, future, supported_searchers):

        processes = []
        results = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            for search in supported_searchers:
                processes.append(executor.submit(self.call_searcher, search, future))

        for d in processes:
            results.update(d.result())

        return results

    def call_searcher(self, search, future):
        try:
            return {type(search).__name__: search.crack(future)}
        except Exception as e:
            logger.warn(f"{type(search).__name__} [{e}]")
            return {type(search).__name__: False}


# Bug Fixing - API / Domain is currently down


class hashsorg:

    supports = set(["md5", "NTLM", "SHA-1"])
    moduels = ["requests"]
    offline = False

    # How do we implment the API key?

    def crack(self, hash):
        try:
            request = requests.get(
                f"https://hashes.org/api.php?key={key}&query={hash[0]}", timeout=hash[3]
            ).text
        except:
            logger.warn("Couldn't connect to hashesorg")
            return False

        # Check for false positive

        if "null" in request:
            logger.warn("Couldnt connect to hashesorg")
            return False
        if not request:
            logger.warn("Hash seems to be a plain???")
            return False

        output = request.split('":"')[2].split('","')[0]

        # Check for Hex

        if "$HEX[" in output:
            return bytearray.fromhex(
                final_output[5 : len(final_output) - 1]
            ).decode()  # Partions it so that it only contains hex and then decodes it into ASCII

        return output


# Need to support IDS but will wait for format from name-that-hash
class hashcat:

    supports = set(["md5", "NTLM", "sha512"])
    moduels = ["subprocess"]
    offline = True

    # How do we implement the types?? (IDs) and wordlist??

    def crack(self, hash):
        print(hash)
        return False
        for possible_type in range(len(hash[2])):
            command = f"hashcat64.exe -a 0 -m {ids[possible_type]} {hash[0]} {wordlist}"  # >> Can change for better optimization etc.....
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
                    logger.warn("Hashcat not in PATH")
                    return False
                if "./hashcat.hctune: No such file or directory" in str(error):
                    logger.warn("Read the docs on using windows")
                    return False
                logger.warn("Hashcat couldn't crack hash")
                continue

            possible_output = str(
                sp.check_output(
                    f"{command} --show", shell=True, cwd="/mnt/p/Hashcat"
                ).strip()
            ).strip("'")

            if not "No hashes loaded." in possible_output:
                return possible_output.split(":")[1]


# Do later
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


# Completed
class LmRainbowTabels:

    # Ok so bug for this one, it doesnt like any word longer then 7 charcters :*(, also it for some reason puts it ALL in caps wtf?

    supports = set(["lm"])

    def crack(self, hash):

        url = "http://rainbowtables.it64.com:80/p3.php"

        payload = f"hashe={hash[0]}&ifik=+Submit+&forma=tak"
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
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            response = requests.request(
                "POST", url, data=payload, headers=headers, timeout=hash[3]
            ).text.split("&nbsp;")
        except:
            logger.warn("Couldn't connect to LM rainbow tabels")
            return False

        if "CRACKED" in response[3]:
            return response[5]

        if "Not yet in database" in response[3]:
            logger.warn("LmRainbowTabels couldnt crack hash")
            return False

        if "Uncrackable with this charset" in response[3]:
            logger.warn("This isnt an LM hash.")
            return False


# OPTIMIZATIONNNNN
class md5crypt:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512", "ntlm"])

    def crack(self, hash):
        for type in hash[1]:
            if type not in supports:
                break
            res = self.search_one_type(hash[0], type)
            if res != False:
                return res
        return False

    def search_one_type(self, hash, type):
        response = requests.get(
            f"https://md5decrypt.net/Api/api.php?hash={hash}&hash_type={type}&email=deanna_abshire@proxymail.eu&code=1152464b80a61728",
            timeout=hash[3],
        ).text
        if len(response) != 0:
            if "CODE ERREUR : 004" in response:
                return False
            return response.strip("\n")
        else:
            return False


# Bug fixing, should be all good
class nitrxgen:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "ntlm"])

    def crack(self, hash):
        response = requests.get(
            "https://www.nitrxgen.net/md5db/" + hash[0], verify=False, timeout=hash[3]
        ).text

        if response:
            # Check for Hex

            if "$HEX[" in response:
                return bytearray.fromhex(
                    response[5 : len(response) - 1]
                ).decode()  # Partions it so that it only contains hex and then decodes it into ASCII
            
            return response

        else:
            logger.warn("Couldn't connect to nitrxegen or couldnt find a hash")
            return False


# Will try and multi-thread later
