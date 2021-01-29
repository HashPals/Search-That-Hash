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
                    # logger.debug("Hashcat not in PATH")
                    return "Failed"
                if "./hashcat.hctune: No such file or directory" in str(error):
                    # logger.debug("Read the docs on using windows")
                    return "Failed"
                # logger.debug("Hashcat couldn't crack hash")
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
