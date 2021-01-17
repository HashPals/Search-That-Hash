def HashesOrg(hashed, key):
    try:
        output = requests.get(f"https://hashes.org/api.php?key={key}&query={hashed}", timeout=5).text
    except:
        print("Couldn't connect")
        return False

    # Check for false positive

    if "null" in output:
        print("Hash not found") ; return False
    if "" == output:
        print("Hash seems to be a plain?") ; return False

    final_output = output.split('":"')[2].split('","')[0]

    # Check for Hex

    if "$HEX[" in final_output:
        final_output = bytearray.fromhex(final_output[5 : len(final_output) - 1]).decode()

    print(f"Found - {final_output}")

    return True

HashesOrg("","")