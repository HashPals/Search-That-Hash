<p align="center">
<img src="Pictures/logo.gif">
</p>

# Work in progress. Not released yet!

# HashSearch
🔎Searches Hash APIs and Google to crack your hash quickly🔎

Don't spend time cracking simple hashes which are found via APIs. Only crack the ones that aren't found!

If your hash is not found via Google or APIs, it will automatically detect the type and crack it.

# Features
* API first. Built for Ciphey, easy to use API.
* Use your own API keys or use free API services.
* Google search for single hashes.
* Automatic identification of hashes.
* Pipes into John / HashCat if hashes are not found in APIs.
* Caching technology. Have the same hash twice in the file? You won't need to crack it twice.
* Multi threaded, of course.

More of a project to aid Ciphey than a project in of itself.

# ToDo
- [x] Use HashID to find possible hashes and mode of hash
- [x] Add config file
- [x] Add argument parsing
- [x] Use only APIs that match these possible hashes
- [x] Add functions of providers
- [x] Multi thread the search calls
- [ ] Design README
  - [ ] gifs (terminalizer)
  - [ ] features
  - [ ] Speed
- [ ] Build more documentation
- [x] https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
- [X] Add config file so users can input their API keys (if they need them)
- [ ] Include Google search parsing (parse HASH:plaintext)
- [ ] If popular hash in set, do that one first
- [ ] Call Hashcat (Default with mode) or John with the mode.