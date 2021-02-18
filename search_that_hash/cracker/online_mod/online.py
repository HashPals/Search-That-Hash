import requests
import json


class LmRainbowTabels:

    # it doesnt like any word longer then 7 charcters :*(, also it for some reason puts it ALL in caps wtf?

    supports = set(["lm"])

    def crack(self, config):

        url = "http://rainbowtables.it64.com:80/p3.php"

        payload = f"hashe={config['chash']}&ifik=+Submit+&forma=tak"
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
                "POST", url, data=payload, headers=headers, timeout=config["timeout"]
            ).text.split("&nbsp;")
        except:
            return "Not connected"

        if "CRACKED" in response[3]:
            return response[5]
        if "Not yet in database" in response[3]:
            return "Failed"
        if "Uncrackable with this charset" in response[3]:
            return "Failed"


class md5crypt:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(
        ["md5", "md4", "ntlm", "sha-1", "sha-256", "sha-384", "sha-512", "ntlm"]
    )

    def crack(self, config):
        for type in config["supported_types"]:
            filtered_type = type.replace(
                "-", ""
            )  # Md5crypt uses sha256, instead of sha-256 which is what NTH gives you
            if type not in self.supports:
                continue

            result = self.search_one_type(hash, filtered_type)

            if result:
                return result

        return "Failed"

    def search_one_type(self, hash, type):
        response = requests.get(
            f"https://md5decrypt.net/Api/api.php?hash={config['chash']}&hash_type={type}&email=deanna_abshire@proxymail.eu&code=1152464b80a61728",
            config["timeout"],
        ).text
        if len(response) != 0:
            if "CODE ERREUR : 004" in response:
                return None
            if "CODE ERREUR : 005" in response:
                return None
            return response.strip("\n")
        else:
            return None


# Bug fixing, should be all good
class nitrxgen:
    # From HashBuster https://github.com/s0md3v/Hash-Buster/blob/master/hash.py
    supports = set(["md5"])

    def crack(self, config):
        response = requests.get(
            "https://www.nitrxgen.net/md5db/" + config["chash"], config["timeout"]
        ).text

        if response:
            # Check for Hex

            if "$HEX[" in response:
                return bytearray.fromhex(
                    response[5 : len(response) - 1]
                ).decode()  # Partions it so that it only contains hex and then decodes it into ASCII

            return response

        else:
            return "Failed"


class cmd5:

    supports = set(["md5", "ntlm", "sha-1", "sha-256", "sha-512", "mysql", "md4"])

    def crack(self, config):

        burp0_url = "https://www.cmd5.org:443/"
        burp0_cookies = {
            "ASP.NET_SessionId": "aaaaaaaaaaaaaaaaaaaaaaaa",
            "FirstVisit": "28/01/2021 2:50:19 AM",
            "Hm_lvt_0b7ba6c81309fff7ce4498ec7b107c0b": "0000000000",
            "Hm_lpvt_0b7ba6c81309fff7ce4498ec7b107c0b": "0000000000",
        }
        burp0_headers = {
            "Connection": "open",
            "Cache-Control": "max-age=1",
            "Upgrade-Insecure-Requests": "0",
            "Origin": "https://www.cmd5.org",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4281.88 Safari/537.36",
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
            "ctl00$ContentPlaceHolder1$TextBoxInput": config["chash"],
            "ctl00$ContentPlaceHolder1$InputHashType": "md5",
            "ctl00$ContentPlaceHolder1$Button1": "decrypt",
            "ctl00$ContentPlaceHolder1$HiddenField1": "",
            "ctl00$ContentPlaceHolder1$HiddenField2": "v/igYz1K/yDDlnTvRIWQYtuyklAdCNOEefJsT96P0wIkSxKQeyxfomZ8W45XFdNl",
        }

        try:
            text = requests.post(
                burp0_url,
                headers=burp0_headers,
                cookies=burp0_cookies,
                data=burp0_data,
                timeout=config["timeout"],
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

    def crack(self, config):
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
            "Connection": "open",
        }
        burp0_data = {"md5": config["chash"], "x": "13", "y": "10"}

        try:
            text = requests.post(
                burp0_url,
                headers=burp0_headers,
                cookies=burp0_cookies,
                data=burp0_data,
                timeout=config["timeout"],
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

    def crack(self, config):
        try:
            out = requests.get(
                f"https://md5.gromweb.com/?md5={config['chash']}",
                timeout=config["timeout"],
            ).text
            text = "".join(
                out.split(
                    '<input class="field" id="form_string_to_hash_string" type="search" name="string" value="'
                )[1]
            ).split('"')[0]
            if not text:
                return "Failed"
            return text
        except:
            return "Not connected"


class sha1_grom:

    supports = set(["sha-1"])

    def crack(self, config):
        try:
            out = requests.get(
                f"https://sha1.gromweb.com/?hash={config['chash']}",
                timeout=config["timeout"],
            ).text
            text = "".join(
                out.split(
                    '<input class="field" id="form_string_to_hash_string" type="search" name="string" value="'
                )[1]
            ).split('"')[0]
            if not text:
                return "Failed"
            return text
        except:
            return "Not connected"


class opcrack:

    supports = set(["ntlm", "lm"])

    def crack(self, config):
        try:
            burp0_url = "https://cracker.okx.ch:443/crack"
            burp0_headers = {
                "Connection": "open",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Content-Type": "application/json",
                "Origin": "https://www.objectif-securite.ch",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.objectif-securite.ch/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            }
            burp0_json = {"value": config["chash"]}

            text = requests.post(
                burp0_url,
                headers=burp0_headers,
                json=burp0_json,
                timeout=config["timeout"],
            ).text

            return "".join(text.split('":"')[1]).split('"}')[0]
        except:
            return "Not connected"


class rainbow_tabels:

    supports = set(["sha-256", "md5", "md4", "ntlm"])

    def crack(self, config):
        try:
            out = requests.get(
                f"https://hashdecryption.com/decrypt.php?str={config['chash']}&send=Submit",
                config["timeout"],
            ).text
            return "".join(out.split("</b> is <b>")[1]).split("</b><br>")[0]
        except:
            return "Failed"


# Bug Fixing - API / Domain is currently down


class hashsorg:

    supports = set(["md5", "ntlm", "sha-1", "md4"])
    moduels = ["requests"]
    offline = False

    def crack(self, config):
        try:
            request = requests.get(
                f"https://hashes.org/api.php?key={key}&query={config['chash']}",
                config["timeout"],
            ).text
        except:
            return "Not connected"

        # Check for false positive

        if "null" in request:
            return "Not connected"
        if not request:
            return "Hash seems to be a plain'"

        output = request.split('":"')[2].split('","')[0]

        # Check for Hex

        if "$HEX[" in output:
            return bytearray.fromhex(final_output[5 : len(final_output) - 1]).decode()
            # Partions it so that it only contains hex and then decodes it into ASCII

        return output
