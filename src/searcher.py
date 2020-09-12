import requests
import re
from concurrent.futures import ThreadPoolExecutor
from collections import namedtuple


class Searcher:
    """
    Searches APIs and Google for your hash
    """

    def __init__(self, config):
        searchers = [hashtoolkit(), nitrxgen(), md5crypt()]
        # , nitrxgen(), md5crypt()
        Hash_input = namedtuple("Hash_input", "text hash_type api_keys")
        futures = []
        results = {}
        for hash in config["hashes"]:
            hash_ctext = next(iter(hash.keys()))

            for search in searchers:
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

                future = Hash_input(hash_ctext, types, keys)

                self.threaded_search(future, supported_searchers)

    def threaded_search(self, future, supported_searchers):

        processes = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            running_tasks = [
                executor.submit(self.call_searcher(search, future)) for search in supported_searchers
            ]
        # for _ in concurrent.futures.as_completed(processes):
        #   print('Result: ', _.result())

        # from concurrent.futures import ThreadPoolExecutor

    def call_searcher(self, search, future):
        try:
            search.crack(future)
        except Exception as e:
            print(f"Error. Searcher {type(search).__name__} is down.")
            return False

def google_search():
    # searches google
    pass


class hashtoolkit:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])

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

    def crack(self, hash_obj):
        for t in hash_obj.hash_type:
            res = search_one_type(hash_obj, t)
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


class hashes_dot_org:
    supports = set(
        [
            "SHA1BCRYPT-CUSTOM",
            "WORDPRESS",
            "PHPBB3",
            "SHA1DASH",
            "DESCRYPT",
            "MD5CRYPT",
            "MD5APR1",
            "SHA512CRYPT",
            "SHA256CRYPT",
            "MD5",
            "SHA1LSB32",
            "SHA1LSB35",
            "SHA1",
            "SHALINKEDIN",
            "MD4",
            "MD2",
            "NTLM",
            "LM",
            "SHA512XORWRL",
            "SHA256",
            "SHA512",
            "SHA224",
            "SHA384",
            "RIPEMD128",
            "RIPEMD160",
            "RIPEMD256",
            "RIPEMD320",
            "WRL0",
            "WRL1",
            "WRL",
            "TIGER2",
            "TIGER128-3",
            "TIGER128-4",
            "TIGER160-3",
            "TIGER160-4",
            "TIGER192-3",
            "TIGER192-4",
            "SNEFRU0",
            "SNEFRU256",
            "GOST-CRYPTO",
            "GOST",
            "ADLER32",
            "CRC32A",
            "CRC32B",
            "HAVAL128-3",
            "HAVAL128-4",
            "HAVAL128-5",
            "HAVAL160-3",
            "HAVAL160-4",
            "HAVAL160-5",
            "HAVAL192-3",
            "HAVAL192-4",
            "HAVAL192-5",
            "HAVAL224-3",
            "HAVAL224-4",
            "HAVAL224-5",
            "HAVAL256-3",
            "HAVAL256-4",
            "HAVAL256-5",
            "MYSQL5TOT",
            "MYSQL5LCTOT",
            "MYSQL5LC",
            "MYSQL5",
            "HMACMD5",
            "HMACSHA1",
            "HMACRIPEMD160",
            "HMACSALTRIPEMD160",
            "BASE64",
            "TRUNC18",
            "RADMIN2",
            "MYSQL3",
            "HALFMD5",
            "RHALFMD5",
            "IPB",
            "SMF",
            "JOOMLA",
            "OSCOMMERCE",
            "MYBB",
            "VBULLETIN",
            "BCRYPT",
            "PBKDF2",
            "HESK-SHA1",
            "HESK-MD5",
            "HESK-SHA256",
            "RAW",
            "DCAB-MD5",
            "BCAD-MD5",
            "CDAB-MD5",
            "HUM",
            "RHUM",
            "DRUPAL7",
            "KECCAK224",
            "KECCAK256",
            "KECCAK384",
            "KECCAK512",
            "KECCAK-SHAKE256",
            "KECCAK-SHAKE512",
            "NSLDAP",
            "HAS-160",
            "CRC32",
            "TTH-HEX",
            "TTH",
            "EDON256",
            "EDON512",
            "BLAKE224",
            "BLAKE256",
            "BLAKE384",
            "BLAKE512",
            "BMW224",
            "BMW256",
            "BMW384",
            "BMW512",
            "CUBE224",
            "CUBE256",
            "CUBE384",
            "CUBE512",
            "ECHO224",
            "ECHO256",
            "ECHO384",
            "ECHO512",
            "FUGUE224",
            "FUGUE256",
            "FUGUE384",
            "FUGUE512",
            "GROESTL224",
            "GROESTL256",
            "GROESTL384",
            "GROESTL512",
            "HAMSI224",
            "HAMSI256",
            "HAMSI384",
            "HAMSI512",
            "JH224",
            "JH256",
            "JH384",
            "JH512",
            "LUFFA224",
            "LUFFA256",
            "LUFFA384",
            "LUFFA512",
            "SHA3-224",
            "SHA3-256",
            "SHA3-384",
            "SHA3-512",
            "PANAMA",
            "RADIOGATUN32",
            "RADIOGATUN64",
            "SHABAL192",
            "SHABAL224",
            "SHABAL256",
            "SHABAL384",
            "SHABAL512",
            "SHAVITE224",
            "SHAVITE256",
            "SHAVITE384",
            "SHAVITE512",
            "SIMD224",
            "SIMD256",
            "SIMD384",
            "SIMD512",
            "SKEIN224",
            "SKEIN256",
            "SKEIN384",
            "SKEIN512",
            "RO13",
            "DANIWEB",
            "DJANGOSHA1",
            "WATTPAD",
            "ARMORGAMES",
            "RUBY",
            "AUTHME",
        ]
    )

    def crack(self, hash_obj):
        if apikey == "":
            return False
        response = requests.get(
            "https://hashes.org/api.php?key={apikey}&query={hashvalue}", timeout=3
        ).json()
        res = response["result"][hashvalue]
        if res == "null":
            return False
        else:
            return res["plain"]
