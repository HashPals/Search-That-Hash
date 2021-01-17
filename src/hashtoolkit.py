import cloudscraper, requests

def hashtoolkit(hash):
	try:
		Scraper = cloudscraper.create_scraper()
		HTML = Scraper.get(f"https://hashtoolkit.com/decrypt-hash/?hash={hash}", timeout=5).text.splitlines()
	except:
		print("Failed to connect to hashtoolkit") ; return False

	for i in range(len(HTML)):
		if "/generate-hash/?text=" in HTML[i]:

			output = HTML[i].partition("?text=")[2].split('">')[0]

			if "</a></span>" in output or 'title"' in output:
				print("Hash not found") ; return False
			else:
				print(f"Hashtoolkit hash found ¦ {output}") ; return True

	print("Hash not found") ; return False

hashtoolkit("5F4DCC3B5AA765D61D8327DEB882CF99")
