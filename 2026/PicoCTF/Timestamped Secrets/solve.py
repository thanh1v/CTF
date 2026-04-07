from hashlib import sha256
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

timestamp = 1770242633
ciphertext = "6d8330b05a68848fdf4b7ab057cd6eb070810e3febd76872b4a5e7627221a396"
def decrypt(ciphertext: str, timestamp: int) -> str:
    key = sha256(str(timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    padded = cipher.decrypt(bytes.fromhex(ciphertext))
    return pad(padded, AES.block_size).decode()

if __name__ == "__main__":
    plaintext = decrypt(ciphertext, timestamp)
    print(f"Decrypted plaintext: {plaintext}")