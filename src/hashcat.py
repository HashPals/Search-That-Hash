import subprocess as sp
def hashcat(hash, ids, wordlist):
    for possible_type in range(len(ids)):
        command = f"hashcat -a 0 -m {ids[possible_type]} {hash} {wordlist}" # >> Can change for better optimization etc.....
        # Hashcat64.exe for windows
        try:
            sp.check_call(
                command,
                shell="True",
                # cwd='/mnt/p/Hashcat' << For windows, you must put the hashcat directory for it to work. Also the wordlist must be in the directory or a full path.
                # stderr=sp.STDOUT
            )
        except sp.CalledProcessError as error:
            if "'hashcat' is not recognized as an internal or external command" in str(error):
                print("Hashcat not in PATH / dir") ; return False
            if "./hashcat.hctune: No such file or directory" in str(error):
                print("Invalid wordlist") ; return False
            print("Couldn't crack")
            continue

        try:
            possible_output = str(
                sp.check_output(
                    f"{command} --show", shell=True, cwd='/mnt/p/Hashcat'
                ).strip()
            ).replace("'","")
        except:
            print("Hash not cracked :/")
        else:
            if not "No hashes loaded." in possible_output:
                print(f"\nHashcat Success ¦ Type {ids[possible_type]} ¦ {possible_output.split(':')[1]}")
                return True

    return False

    ''' Notes

    check_call >> shows output
    check_output >> hides output

    Checks .pot file with --show to see if hash has alredy been cracked

    Can change the base varible command to use different settings and such

    '''

hashcat('0EAAB3F6E2B748D472124AAB728CE18A',['1000'],"example.txt")
