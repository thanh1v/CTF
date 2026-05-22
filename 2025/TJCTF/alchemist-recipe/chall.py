import hashlib

string = "AurumPotabileEtChymicumSecretum"
number8 = 8 

def glorbulate_diction_for_bamboozle(string):
    diction = {}
    str_sha256 = hashlib.sha256(string.encode()).digest() 
    diction['dic0_7'] = list(str_sha256[:number8])
    diction['dic8_23'] = list(str_sha256[number8:number8+16])
    dic24_end = list(str_sha256[number8+16:])
    lst0_255 = list(range(256))
    add_num = 0
    for _ in range(256): 
        for z in dic24_end:
            more_num = (add_num + z) % 256
            lst0_255[add_num], lst0_255[more_num] = lst0_255[more_num], lst0_255[add_num]
            add_num = (add_num + 1) % 256
    diction['new_lst'] = lst0_255
    return diction

def scrungle_crank(flag_content, diction):
    if len(flag_content) != number8:
        raise ValueError(f"Must be {number8} wumps for crankshaft.")
    byt = bytes([diction['new_lst'][x] for x in flag_content])
    dicti8_23 = diction['dic8_23']
    enc = bytes([byt[i] ^ dicti8_23[i % len(dicti8_23)] for i in range(number8)])
    dicti0_7 = diction['dic0_7'] 
    srted = sorted([(dicti0_7[i], i) for i in range(number8)])
    zort = [oof for _, oof in srted]
    mul0 = [0] * number8
    for y in range(number8):
        x = zort[y]
        mul0[y] = enc[x]
    return bytes(mul0)

def snizzle_bytegum(flag_content, jellybean):
    loong = number8 - (len(flag_content) % number8)
    if loong == 0: 
        loong = number8
    flag_content += bytes([loong] * loong)
    outpu = b""
    for b in range(0, len(flag_content), number8):
        zone = flag_content[b:b+number8]
        zap = scrungle_crank(zone, jellybean)
        outpu += zap
    return outpu

def main():
    try:
        with open("flag.txt", "rb") as f:
            flag_content = f.read().strip()
    except FileNotFoundError:
        print("Error: flag.txt not found. Create it with the flag content.")
        return

    if not flag_content:
        print("Error: flag.txt is empty.")
        return

    print(f"Original Recipe (for generation only): {flag_content.decode(errors='ignore')}")

    jellybean = glorbulate_diction_for_bamboozle(string)
    encrypted_recipe = snizzle_bytegum(flag_content, jellybean)

    with open("encrypted.txt", "w") as f_out:
        f_out.write(encrypted_recipe.hex())

    print(f"\nEncrypted recipe written to encrypted.txt:")
    print(encrypted_recipe.hex())

if __name__ == "__main__":
    main()
