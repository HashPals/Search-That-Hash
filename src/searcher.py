import requests

class Searcher:
    """
    Searches APIs and Google for your hash
    """


class hashtoolkit:
    supports = set("md5", "sha1", "sha256", "sha384", "sha512")
    def crack(hashvalue, hashtype):
        response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hashvalue).text
        match = re.search(r'/generate-hash/?text=.*?"', response)
        if match:
            return match.group(1)
        else:
            return False

class nitrxgen:
    supports = set("md5")

    def crack(hashvalue, hashtype):
        response = requests.get('https://www.nitrxgen.net/md5db/' + hashvalue, verify=False).text
        if response:
            return response
        else:
            return False

def beta(hashvalue, hashtype):
    response = requests.get('https://hashtoolkit.com/reverse-hash/?hash=' + hashvalue).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False

    md5 = [gamma, alpha, beta, theta, delta]
sha1 = [alpha, beta, theta, delta]
sha256 = [alpha, beta, theta]
sha384 = [alpha, beta, theta]
sha512 = [alpha, beta, theta]