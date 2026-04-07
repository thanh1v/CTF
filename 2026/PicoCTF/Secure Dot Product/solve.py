from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = "lonely-island.picoctf.net"
PORT = 51637

r = remote(HOST, PORT)

r.recvuntil(b"IV: ")
iv = bytes.fromhex(r.recvline().strip().decode())

r.recvuntil(b"Ciphertext: ")
ct = bytes.fromhex(r.recvline().strip().decode())

trusted = []

while len(trusted) < 5:
    line = r.recvline().decode().strip()

    if line.startswith("("):
        vec, h = eval(line)
        trusted.append((vec, h))

key = []

for i in range(32):

    payload = "[" + ","*i + "1]"
    fake_hash = trusted[0][1]

    r.sendlineafter(b"Enter your vector: ", payload.encode())
    r.sendlineafter(b"Enter its salted hash: ", fake_hash.encode())

    print(r.recv(timeout=2))
    leak = int(r.recvline().strip())

    key.append(leak)

key = bytes(key)

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct), 16)

print(flag)