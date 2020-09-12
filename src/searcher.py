import requests
import re
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple
from functools import lru_cache

class Searcher:
    """
    Searches APIs and Google for your hash
    """

    def __init__(self, config):
        self.searchers = [hashtoolkit(), nitrxgen(), md5crypt(), hashes_dot_org(), hashes_dot_org()]
        self.Hash_input = namedtuple("Hash_input", "text hash_type api_keys")
        self.perform_search(config)


    def perform_search(self, config):
        futures = []
        results = {}
        for hash in config["hashes"]:
            hash_ctext = next(iter(hash.keys()))

            for search in self.searchers:
                # gets hash types
                keys = hash[next(iter(hash.keys()))].keys()
                # converts to lowercase
                keys = [x.lower() for x in keys]

                supported_searchers = []

                # places True in list if it matches
                types = []
                for hashtype in keys:
                    if hashtype in search.supports:
                        supported_searchers.append(search)
                        types.append(hashtype)

                future = self.Hash_input(hash_ctext, types, config["api_keys"])

            self.threaded_search(future, supported_searchers) 

    def threaded_search(self, future, supported_searchers):

        processes = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            running_tasks = [
                executor.submit(self.call_searcher(search, future))
                for search in supported_searchers
            ]
        print(running_tasks)
            for _ in concurrent.futures.as_completed(processes):
                print('Result: ', _.result())

        # from concurrent.futures import ThreadPoolExecutor

    def call_searcher(self, search, future):
        try:
            search.crack(future)
        except Exception as e:
            print(e)
            print(f"Error. Searcher {type(search).__name__} is down.")
            return False


def google_search():
    # searches google
    pass


class hashtoolkit:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])
    @lru_cache
    def crack(self, hash_obj):
        response = requests.get(
            "https://hashtoolkit.com/reverse-hash/?hash=" + hash_obj.text, timeout=3
        ).text
        match = re.search(r'/generate-hash/?text=.*?"', response)
        if match:
            return match.group(1)
        else:
            return False


class nitrxgen:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5"])
    @lru_cache
    def crack(self, hash_obj):
        response = requests.get(
            "https://www.nitrxgen.net/md5db/" + hash_obj.text, verify=False, timeout=1
        ).text
        if response:
            return response
        else:
            return False


class md5crypt:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])
    @lru_cache
    def crack(self, hash_obj):
        for t in hash_obj.hash_type:
            res = self.search_one_type(hash_obj, t)
            if res != False:
                return res
        return False
    @lru_cache
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


class hashes_dot_org:
    supports = set(
        [
            "bcad-md5",
            "mysql3",
            "haval160-4",
            "crc32b",
            "bmw512",
            "armorgames",
            "hesk-sha1",
            "hamsi256",
            "luffa384",
            "sha1lsb32",
            "smf",
            "mysql5lc",
            "vbulletin",
            "sha3-384",
            "md5crypt",
            "wrl",
            "skein512",
            "gost-crypto",
            "sha384",
            "haval224-5",
            "tiger128-3",
            "rhalfmd5",
            "hesk-sha256",
            "has-160",
            "halfmd5",
            "blake512",
            "cube256",
            "keccak256",
            "fugue384",
            "ruby",
            "sha256",
            "crc32",
            "shalinkedin",
            "skein224",
            "wrl0",
            "keccak-shake256",
            "edon512",
            "shavite384",
            "keccak384",
            "simd256",
            "phpbb3",
            "jh224",
            "sha1lsb35",
            "ripemd320",
            "mysql5lctot",
            "cube384",
            "blake256",
            "oscommerce",
            "blake224",
            "tth",
            "hmacripemd160",
            "sha512",
            "wordpress",
            "jh512",
            "daniweb",
            "echo384",
            "ripemd160",
            "tiger160-4",
            "snefru256",
            "shavite256",
            "hum",
            "luffa224",
            "fugue224",
            "sha1bcrypt-custom",
            "descrypt",
            "cube512",
            "djangosha1",
            "sha3-256",
            "hmacmd5",
            "tiger2",
            "haval128-4",
            "md4",
            "haval224-4",
            "md5apr1",
            "raw",
            "drupal7",
            "snefru0",
            "hmacsha1",
            "jh384",
            "hamsi384",
            "haval224-3",
            "ipb",
            "simd384",
            "wrl1",
            "shabal256",
            "haval192-3",
            "keccak224",
            "echo256",
            "groestl384",
            "hamsi512",
            "sha1",
            "simd224",
            "tiger160-3",
            "radmin2",
            "luffa512",
            "hesk-md5",
            "shavite512",
            "wattpad",
            "radiogatun64",
            "haval128-5",
            "radiogatun32",
            "skein256",
            "mysql5",
            "echo224",
            "tiger192-4",
            "haval192-5",
            "tth-hex",
            "jh256",
            "haval256-3",
            "panama",
            "echo512",
            "lm",
            "trunc18",
            "ntlm",
            "haval256-4",
            "pbkdf2",
            "haval128-3",
            "tiger128-4",
            "authme",
            "ro13",
            "luffa256",
            "tiger192-3",
            "gost",
            "shabal384",
            "md2",
            "adler32",
            "groestl256",
            "bmw256",
            "crc32a",
            "hamsi224",
            "nsldap",
            "bcrypt",
            "bmw224",
            "skein384",
            "base64",
            "sha512xorwrl",
            "hmacsaltripemd160",
            "fugue256",
            "shabal224",
            "fugue512",
            "haval160-3",
            "cdab-md5",
            "ripemd128",
            "groestl224",
            "md5",
            "ripemd256",
            "edon256",
            "bmw384",
            "simd512",
            "keccak-shake512",
            "shavite224",
            "cube224",
            "sha3-512",
            "shabal512",
            "haval192-4",
            "keccak512",
            "joomla",
            "sha1dash",
            "shabal192",
            "sha512crypt",
            "mybb",
            "blake384",
            "haval256-5",
            "groestl512",
            "rhum",
            "dcab-md5",
            "sha224",
            "haval160-5",
            "mysql5tot",
            "sha3-224",
            "sha256crypt",
        ]
    )

    def crack(self, hash_obj):
        if hash_obj.api_keys == None:
            return False
        response = requests.get(
            "https://hashes.org/api.php?key={hash_obj.api_keys['hashes_dot_org']}&query={hash_obj.text}", timeout=3
        ).json()
        res = response["result"][hashvalue]
        if res == "null":
            return False
        else:
            return res["plain"]
