import hashlib

# Cấu hình giống như mã gốc
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

def reverse_scrungle_crank(block, diction):
    dicti8_23 = diction['dic8_23']
    dicti0_7 = diction['dic0_7']
    new_lst = diction['new_lst']

    # Tạo thứ tự zort như trong mã gốc
    srted = sorted([(dicti0_7[i], i) for i in range(number8)])
    zort = [oof for _, oof in srted]

    # Giải mã theo thứ tự ngược lại
    enc = [0] * number8
    for y in range(number8):
        x = zort[y]
        enc[x] = block[y]

    # XOR ngược với dic8_23
    xor_back = [enc[i] ^ dicti8_23[i % len(dicti8_23)] for i in range(number8)]

    # Map ngược từ new_lst để tìm lại chỉ số ban đầu
    reverse_map = [0] * 256
    for i, val in enumerate(new_lst):
        reverse_map[val] = i

    original = bytes([reverse_map[b] for b in xor_back])
    return original

def decrypt_flag(cipher_hex):
    encrypted = bytes.fromhex(cipher_hex)
    jellybean = glorbulate_diction_for_bamboozle(string)

    plaintext = b""
    for i in range(0, len(encrypted), number8):
        block = encrypted[i:i+number8]
        decoded = reverse_scrungle_crank(block, jellybean)
        plaintext += decoded

    # Loại bỏ padding PKCS#7
    pad = plaintext[-1]
    if all(p == pad for p in plaintext[-pad:]):
        plaintext = plaintext[:-pad]
    return plaintext

# Chuỗi mã hóa bạn cung cấp
cipher_hex = "b80854d7b5920901192ea91ccd9f588686d69684ec70583abe46f6747e940c027bdeaa848ecb316e11d9a99c7e87b09e"

# Giải mã
flag = decrypt_flag(cipher_hex)
print("🎉 Recovered Flag:", flag.decode(errors="ignore"))
