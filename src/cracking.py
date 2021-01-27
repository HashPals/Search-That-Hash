import warnings as logger
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
import requests
from rich.console import Console

console = Console()
logger.filterwarnings("ignore")

# This is an example input

# TODO :
# Get logru warnings
#

class Searcher:

    def __init__(self, config):
        self.config = config
        self.searchers_offline = [
            hashcat()
        ]  
        self.searchers_online = [
            hashsorg(),
            LmRainbowTabels(),
            nitrxgen(),
            md5crypt(),
            cmd5(),
            md5_addr(),
            md5_grom(),
            sha1_grom()
        ]
        self.Hash_input = namedtuple(
            "Hash_input", ["text", "types", "hashcats", "api_keys", "timeout"]
        )

    def main(self):

        return(self.perform_search(self.config))

    def perform_search(self, config):

        if not config["timeout"]:
            config["timeout"] = 1

        # print(config["timeout"])

        for hash, types in config["hashes"].items():
            hash_ctext = hash

            keys = [type["name"].lower() for type in types]
            hashcats = [type["hashcat"] for type in types]

            # print(keys)

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

            return(self.threaded_search(future, supported_searchers))

    def threaded_search(self, future, supported_searchers):

        processes = []
        success = {}
        fails = {}

        with ThreadPoolExecutor(max_workers=4) as executor:
            for search in supported_searchers:
                processes.append(executor.submit(self.call_searcher, search, future))

        for d in processes:
          if list(d.result().values())[0] == "Failed" or list(d.result().values())[0] == "Not connected":
            fails.update(d.result())
          else:
            success.update(d.result())
          #results.update(d)
        return({future[0] : [success, fails]})

    def call_searcher(self, search, future):
        try:
            return {type(search).__name__: search.crack(future)}
        except Exception as e:
            logger.warn(f"{type(search).__name__} [{e}]")
            return {type(search).__name__: "Failed"}


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
            return("Not connected")

        # Check for false positive

        if "null" in request:
            logger.warn("Couldnt connect to hashesorg")
            return "Not connected"
        if not request:
            logger.warn("Hash seems to be a plain???")
            return "Hash seems to be a plain'"

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
        return "Failed"
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
                    return "Failed"
                if "./hashcat.hctune: No such file or directory" in str(error):
                    logger.warn("Read the docs on using windows")
                    return "Failed"
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
            return "Not connected"

        if "CRACKED" in response[3]:
            return response[5]

        if "Not yet in database" in response[3]:
            logger.warn("LmRainbowTabels couldnt crack hash")
            return "Failed"

        if "Uncrackable with this charset" in response[3]:
            logger.warn("This isnt an LM hash.")
            return "Failed"


# OPTIMIZATIONNNNN
class md5crypt:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1a-", "sha-256", "sha384", "sha512", "ntlm"])

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
            return "Failed"


class cmd5:

    supports = set(["md5", "ntlm", "sha-1", "sha-256", "sha-512", "mysql"])

    def crack(self, hash):

        burp0_url = "https://www.cmd5.org:443/"
        burp0_cookies = {
            "ASP.NET_SessionId": "qlif5gdwpbwtgetadf1joxox",
            "FirstVisit": "1/27/2021 2:50:19 AM",
            "Hm_lvt_0b7ba6c81309fff7ce4498ec7b107c0b": "1611687026",
            "Hm_lpvt_0b7ba6c81309fff7ce4498ec7b107c0b": "1611687026",
        }
        burp0_headers = {
            "Connection": "close",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://www.cmd5.org",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.cmd5.org/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }
        burp0_data = {
            "__EVENTTARGET": "Button1",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": "tu3WNlNyUoktOeZhTvcpBgoQNoH8wLOeqDzVGEU8XUzmvViF7uaTr0g08l0kUf5lk3qITzThnkc2nUW1yLwFIjQ47H1XJ0OGnrfH/bM7kxSAW+uqvNVB0XvbJzA7l8DxDZt9HphWM+ettS5HAmW1L2a8tdflHF4/YkDL9ZHzu78ZpQwFoo8R8S7uSLVj2rOlV68Tprep6JyNStYF5JyKlbyrIZbJgwmRl9Y1KY2qQHTRgEmYA/CUveeY2AK+AAbOBM0STCWbdvMwaGwCKR5lXpdbmWUCBhi2cFzG7blTzkUWTaorAvUNqldJ9Jrr1XB7EsbsSgQwLvif70ztu3/M0FptuoUCbuMlEOWYh1YE+im3RripucSN9SKxwO4TRfk7Y46bm2asXHDsHXDa/uWr/301DHVRiii0Rnd7XXg2TNtyuhUt+VOlye6ZQBSuQ75L8tFKMpCnWs6xMUNGxz1IICxDmbHxPBx6NUdis9RYjh1cd+xcF1I+84jz8F2nwTpEN51D+eWLKMB5ZFrb4tExNZhNtRJ6vKbX9ntv+N9Ktg0Hmq3mu43FlGRP5H7pWdhdO3a8HdyX1vs1fF8izfMidpN/Sh4jcozbUAIbXtJDjnCMo8P2vCOS8MvNntcA1pHakoDEZIaVKkD8Q9XK9Az76kgJEFG9f4mV1/3xdQDHZZOnTymz09CrB7VKb+yd1Y2jCkHPger5mYNrKdtFrnFzFNeTycln/mybXwHIXLLv/VUHUPv+m15IlomAvQggWcjOXyTGjlNRE4V+1Jn6Fsr8QdG8qV6zC8lDM0GU2++MKOxLgOfxX/TjnycruULcAbYCgfY6FCdfqXBuNp1OK+CCNvI3emhA+olMzsykpONescFHlmKuH/UUvvx5CtVw4T8aYfhpLduzMi7smG41BcPw9xjKvFCACOVGM6aa5WrHOzdWgZJd+Cpa5BUdoOfiwHZyzuvtWBbwbaWafqjsxisXhEWMODkrdN+kChxX93KGU6I5bxRIQZHJge540/Cv1mElRimxNo8IyrzFK/ek5Pezjj/TWY63ERN82kastXX/SYLGu1KkSSaUsIus8WTI+hxjhFvks8vX9IyxBsm3iWKKFomyx/BK7GeWEn9x6H+RgDpN9crDnaqc8aL/bWK5lKhglMhxOPxR0Cf0f9Mi1bi8VwzuZSpFIIbZYvNngJhz7kqGgZTwdeWhCx0WLd0T3Q74IevoMo1kj819Qgzb3XN9LfDiOkoznj3Ae8uh+HZWVRDjubd9e9PnKrsMmB39VP3LbY2qyTyUWHHNN+GXsX/nxVUrRoXkUe71Q1espbbry+lHN/dc5e/+qR8C8oGLjQ5UhCEAMDRcoXNDWLFLPcyWL2A5Kh/VCPbMUqluJw==",
            "__VIEWSTATEGENERATOR": "CA0B0334",
            "ctl00$ContentPlaceHolder1$TextBoxInput": hash[0],
            "ctl00$ContentPlaceHolder1$InputHashType": "md5",
            "ctl00$ContentPlaceHolder1$Button1": "decrypt",
            "ctl00$ContentPlaceHolder1$HiddenField1": "",
            "ctl00$ContentPlaceHolder1$HiddenField2": "v/igYz1K/yDDlnTvRIWQYtuyklAdCNOEefJsT96P0wIkSxKQeyxfomZ8W45XFdNl",
        }

        try:
            text = requests.post(
                burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout = hash[3]
            ).text
            return "".join(
                text.split(
                    '<span id="LabelAnswer" class="LabelAnswer" onmouseover="toggle();">'
                )[1]
            ).split("<")[0]
        except:
            return "Failed"


class md5_addr:

    supports = set(["md5"])

    def crack(self, hash):
        burp0_url = "http://md5.my-addr.com:80/md5_decrypt-md5_cracker_online/md5_decoder_tool.php"
        burp0_cookies = {"PHPSESSID": "aki2l78uvb3hk5n1uvuhefut17"}
        burp0_headers = {
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "http://md5.my-addr.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "close",
        }
        burp0_data = {"md5": hash[0], "x": "13", "y": "10"}

        try:
            text = requests.post(
                burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data, timeout = hash[3]
            ).text
            return "".join(
                text.split(
                    "<div class='white_bg_title'><span class='middle_title'>Hashed string</span>: "
                )[1]
            ).split("</div")[0]
        except:
            return "Failed"

class md5_grom:

    supports = set(["md5"])

    def crack(self, hash):
        try:
            out = requests.get(f"https://md5.gromweb.com/?md5={hash[0]}", timeout = hash[3]).text
            text = "".join(out.split('<input class="field" id="form_string_to_hash_string" type="search" name="string" value="')[1]).split('"')[0]
            if not text:
                return("Failed")
            return(text)
        except:
            return("Not connected")

class sha1_grom:

    supports = set(["sha-1"])

    def crack(self, hash):
        try:
            out = requests.get(f"https://sha1.gromweb.com/?hash={hash[0]}", timeout = hash[3]).text
            text = "".join(out.split('<input class="field" id="form_string_to_hash_string" type="search" name="string" value="')[1]).split('"')[0]
            if not text:
                return("Failed")
            return(text)
        except:
            return("Not connected")        
    
# Will try and multi-thread later
