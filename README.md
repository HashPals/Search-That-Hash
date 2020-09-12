<p align="center">
<img src="Pictures/logo.gif">
</p>

# HashSearch
🔎Searches Hash APIs and Google to crack your hash quickly🔎

Don't spend time cracking simple hashes which are found via APIs. Only crack the ones that aren't found!

If your hash is not found via Google or APIs, it will automatically detect the type and crack it.

# Features
* API first. Built for Ciphey, easy to use API.
* Use your own API keys or use free API services.
* Don't spend time 

More of a project to aid Ciphey than a project in of itself.

Work in progress. Not released yet!

# ToDo
- [x] Use HashID to find possible hashes and mode of hash
- [x] Add config file
- [x] Add argument parsing
- [x] Use only APIs that match these possible hashes
- [x] Add functions of providers
- [x] Multi thread the search calls
- [ ] Design README
- [ ] Build more documentation
- [x] https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
- [ ] Add config file so users can input their API keys (if they need them)
- [ ] Include Google search parsing (parse HASH:plaintext)
- [ ] If popular hash in set, do that one first
- [ ] Call Hashcat (Default with mode) or John with the mode.

# MVP 1
Import config file as dict
Pass dict to search_and_crack
search for hashes
