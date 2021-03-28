import subprocess as sp

class Hashcat:
    def crack(self, config):

        hashcat_dict = str.maketrans({"$": "\\$"})
        hash_formatted = config["chash"].translate(hashcat_dict)
        
        for possible_type in config["hashcat_types"]:
            
            command = f"cd {config['hashcat_folder']} && {config['hashcat_exe_name']} -a 0 -m {possible_type} {hash_formatted} {config['wordlist']}"
            
            if config["greppable"]:
                config["greppable"] = sp.DEVNULL
            else:
                config["greppable"] = None
            try:
                sp.check_call(
                    command,
                    shell="True",
                    cwd=config["hashcat_binary"],
                    stdout=config["greppable"],
                    stderr=config["greppable"],
                )
            except Exception as e:
                if "returned non-zero exit status 1." in e:
                    continue
                else:
                    return "Failed"
            possible_output = str(
                sp.check_output(
                    f"{command} --show",
                    shell=True,
                    cwd=config["hashcat_binary"],
                ).strip()
            ).strip("'")
            if not "No hashes loaded." in possible_output:
                return possible_output.split(":")[1]

        return "Failed"
