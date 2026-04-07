
from Crypto.Util.number import long_to_bytes

# ciphertext từ output.txt
ct_hex = "21c1b705764e4bfdafd01e0bfdbc38d5eadf92991cdd347064e37444e517d661cea9"
ct = bytes.fromhex(ct_hex)

def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    lfsr = (feedback << 7) | (lfsr >> 1)
    return lfsr

def decrypt(ct, seed):
    lfsr = seed
    pt = bytearray()

    for c in ct:
        lfsr = steplfsr(lfsr)
        ks = lfsr
        pt.append(c ^ ks)

    return bytes(pt)

for seed in range(256):
    pt = decrypt(ct, seed)

    try:
        text = pt.decode()
        if "pico" in text or "flag" in text:
            print("seed:", seed)
            print("plaintext:", text)
    except:
        pass
