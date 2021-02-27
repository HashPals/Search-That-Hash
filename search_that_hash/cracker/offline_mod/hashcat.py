import subprocess as sp


class Hashcat:
    def crack(self, config):

        hashcat_dict = str.maketrans({"$": "\\$"})

        hash_formatted = config["chash"].translate(hashcat_dict)

        for possible_type in config["hashcat_types"]:

            # If its greppable then silence.
            if config["greppable"]:
                if config["hashcat_binary"]:  # If on windows run from binary folder
                    command = f".\\hashcat64.exe -a 0 -m {possible_type} {hash_formatted} {config['wordlist']}"
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                            cwd=config["hashcat_binary"],
                            stdout=sp.DEVNULL,
                            stderr=sp.STDOUT,
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

                else:
                    command = f"hashcat -a 0 -m {possible_type} {hash_formatted} {config['wordlist']}"
                    try:
                        sp.check_call(
                            command, shell="True", stdout=sp.DEVNULL, stderr=sp.STDOUT
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

            else:
                if config["hashcat_binary"]:  # On windows? Run from binary folder
                    command = f"./hashcat64.exe -a 0 -m {possible_type} {hash_formatted} {config['wordlist']}"
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                            cwd=config["hashcat_binary"],
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

                else:
                    command = f"hashcat -a 0 -m {possible_type} {hash_formatted} {config['wordlist']}"
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                        )
                    except Exception as e:
                        if "returned non-zero exit status 1." in e:
                            continue
                        else:
                            return "Failed"

                    possible_output = str(
                        sp.check_output(f"{command} --show", shell=True).strip()
                    ).strip("'")

                    if not "No hashes loaded." in possible_output:
                        return possible_output.split(":")[1]

        return "Failed"
