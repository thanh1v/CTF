from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

p = 8960772424399520512528788347725912280684635790965762798750278716225426056950879995449619263280073105713391945818413565722441814992183882527630562500000001

v = 5728133706618207944390141231027903587001189692552344220411807080039452536350747258001505261278780057108644051176047853253817775449251970128057213426047967

iv = bytes.fromhex(
"86f660f34399c1789ea3835acb5ade24"
)

ciphertext = bytes.fromhex(
"dd054c382b908c09ccb7ee3c3d2ecd3c52b4f51b1ad0fe0a8ac72a853f4663fb004e719c3a4910a4baee0f84a2999429"
)

def try_key(A,B):

    candidates = [
        str(A).encode()+str(B).encode(),
        str(B).encode()+str(A).encode(),
        (str(A)+str(B)).encode(),
    ]

    for data in candidates:
        key = hashlib.sha256(data).digest()[:16]

        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ciphertext),16)

            if b"{" in pt:
                print("[+] FOUND")
                print(pt)
                return True
        except:
            pass
    return False


for q in range(1, 2_000_001):

    A = pow(v, q, p)     # pretty_cabinet guess
    B = pow(2, q, p)     # base guess (common CTF g=2)

    if try_key(A,B):
        break

    if q % 10000 == 0:
        print("tested", q)