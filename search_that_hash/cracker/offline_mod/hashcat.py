class Hashcat:
    def crack(self, hash):

        hashcat_dict = str.maketrans({"$": "\\$"})

        hash_formatted = hash[0].translate(hashcat_dict)

        for possible_type in hash[2]:
            # Is greppable? Yes - Then silence.
            if hash[5]:
                if hash[7]:  # On windows? Run from binary folder
                    command = f".\\hashcat64.exe -a 0 -m {possible_type} {hash_formatted} {hash[6]}"
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                            cwd=hash[7],
                            stdout=sp.DEVNULL,
                            stderr=sp.STDOUT,
                        )
                    except:
                        return "Failed"
                        continue

                    possible_output = str(
                        sp.check_output(
                            f"{command} --show", shell=True, cwd=hash[7]
                        ).strip()
                    ).strip("'")

                    if not "No hashes loaded." in possible_output:
                        return possible_output.split(":")[1]

                else:
                    command = (
                        f"hashcat -a 0 -m {possible_type} {hash_formatted} {hash[6]}"
                    )
                    try:
                        sp.check_call(
                            command, shell="True", stdout=sp.DEVNULL, stderr=sp.STDOUT
                        )
                    except:
                        return "Failed"
                        continue

                    possible_output = str(
                        sp.check_output(
                            f"{command} --show", shell=True, cwd=hash[7]
                        ).strip()
                    ).strip("'")

                    if not "No hashes loaded." in possible_output:
                        return possible_output.split(":")[1]

            else:
                if hash[7]:  # On windows? Run from binary folder
                    command = f"./hashcat64.exe -a 0 -m {possible_type} {hash_formatted} {hash[6]}"
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                            cwd=hash[7],
                        )
                    except:
                        return "Failed"
                        continue

                    possible_output = str(
                        sp.check_output(
                            f"{command} --show", shell=True, cwd=hash[7]
                        ).strip()
                    ).strip("'")

                    if not "No hashes loaded." in possible_output:
                        return possible_output.split(":")[1]

                else:
                    command = (
                        f"hashcat -a 0 -m {possible_type} {hash_formatted} {hash[6]}"
                    )
                    try:
                        sp.check_call(
                            command,
                            shell="True",
                        )
                    except:
                        return "Failed"
                        continue

                    possible_output = str(
                        sp.check_output(f"{command} --show", shell=True).strip()
                    ).strip("'")

                    if not "No hashes loaded." in possible_output:
                        return possible_output.split(":")[1]



