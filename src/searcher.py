import requests


class Searcher:
    """
    Searches APIs and Google for your hash
    """

    def __init__(self, config):
        searchers = [hashtoolkit(), nitrxgen(), md5crypt()]
        results = {}
        for hash in config["hashes"]:
            print(hash)
            for search in searchers:
                # gets hash types
                keys = hash[next(iter(hash.keys()))].keys()
                # converts to lowercase
                keys = [x.lower() for x in keys]
                # places True in list if it matches
                for type in keys:
                    if type in search.supports:
                        print("types match")
                        result = search.crack()
                to_check = [True for i in keys if i in search.supports]
                # Returns True if any of the possible hash types is something the searcher supports
                if any(to_check):
                    print("Types match")
                    result = search.crack()
                    print(result)
                    """
                    if result != False:
                        # remove hash from list and add to dict of results
                        results["hash"] = result
                        config["hashes"].pop(hash)
        return config["results"] = results"""
                    
    

def google_search():
    # searches google
    pass


class hashtoolkit:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])

    def crack(config):
        response = requests.get(
            "https://hashtoolkit.com/reverse-hash/?hash=" + hashvalue
        ).text
        match = re.search(r'/generate-hash/?text=.*?"', response)
        if match:
            return match.group(1)
        else:
            return False


class nitrxgen:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5"])

    def crack(config):
        response = requests.get(
            "https://www.nitrxgen.net/md5db/" + hashvalue, verify=False
        ).text
        if response:
            return response
        else:
            return False


class md5crypt:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5", "sha1", "sha256", "sha384", "sha512"])

    def crack(config):
        response = requests.get(
            "https://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728"
            % (hashvalue, hashtype)
        ).text
        if len(response) != 0:
            return response
        else:
            return False


class hashes_dot_org:
    supports = set([
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
    ])
    def crack(config):
        if apikey == "":
            return False
        response = requests.get("https://hashes.org/api.php?key={apikey}&query={hashvalue}").json()
        res = response["result"][hashvalue]
        if res == "null":
            return False
        else:
            return res["plain"]


