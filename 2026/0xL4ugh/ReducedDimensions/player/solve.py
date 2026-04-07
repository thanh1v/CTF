from Crypto.Util.number import long_to_bytes, inverse, GCD
import sys

# Given values
n = 24436555811992972366076806922530312273907496823566498825278523886197470905017391954938641972382127780163747562797956038193398654235644409459287830339446234525262072627164429789264587184451084484976035579016063031028571643546268940916664832350416704133070528632744931737357768415126788528052461206333395794164406084571633391115829776964808677724703621221154710591190375698378697896449037181113710774632252351521950724961537615755537875194862156989318761303971336544564950137455452434307027177388197740176937447577518701185717201408469263753367188476145954061480542913006467287367140336404472235624010067372903582272729
e = 65537
ciphertext = [7645133316138320672920829866179304735182212690210047500676759675676422841305242219428671895825721777886336067123230090334404443239249744649348019800170870076772170648917374424307951430757942474104583441027037157499352780211088515553775367980514698077272400388982174956856115745318060191675644580097459087877103744768611124967141106979760409192285920050555016687019974731108717211479671838777445410222040882405240324940267527783747870861280181437508731620415299917485800707003438326195859384666421699977525718115984628571014356722832203980578905816041544254774832610446558646617081820383024594943509109272533930838708, 15115864622351599035162706206257324674672546729754571030515410021905207212154731966558659435218498028437041608389247596685777775075531974586762001822195044830215779677969600204017249097853619421972862952306880626946718048703037486579156521083427871219972900601347265611525515981798763462306348832427757653091251117371763790691703299928013908976268558111890052847761824740201601000159794443256033087429920731339521534477358144537370658535238347192547096515188805816620173560028595429243354057894242958704409904709847929320587768434722670465044376198153825572537650025403520767434960328371498100779394191999106392405505, 13745229990855433471733323096856618171809729836071048905352245517395661673128741357306382928377040374671176807926741135701004188571412113925163459038871795016583126047331363592533678987966281886904921753115792048974820789657695172533157583206166353580229326903802517936396022419823884208200013314323762420208768560108045572583904747823741147655693248507409489075089305887965790292485140729487526433929859183972759579430813209494595211145046105006826362941878536200003370316700559144884743367020754865964581608047339157411175462078984500914717760473129611002520677145892778242279106724152108492680282436100305414987989, 13075867308307993713881388617739767319783540136821062304673039023416514479073968404704931053707431722417113432221377192698845939724954608884902350188774482318948356490572584570493016148272003096623369096838093349374805909370089074902960407209272664510740999775809485842810426515913298045223326669961556520541238694804400787951685561362702557941491071370737013429166029262325140106903158536926574942320103807698268441557280143112008091660020312242173901777414105294912109492658141997518018221759802285312329937197750464541705293605084821535959702107937728040393887374381496534531147546227981215469580847563998832887560]

print("[*] Analyzing challenge structure...")
print("[*] The ciphertext is the first row of A^e mod n")
print("[*] Where A is the quaternion matrix for (m, m+3p+7q, m+11p+13q, m+17p+19q)")
print()

# The first row of the quaternion matrix is [a0, -a1, -a2, -a3]
# So ciphertext[0] corresponds to the first element of (A^e)[0]
# This is a complex polynomial in a0, a1, a2, a3

# Key insight: The determinant of the quaternion matrix is the norm^2
# det(A) = (a0^2 + a1^2 + a2^2 + a3^2)^2
# And det(A^e) = det(A)^e

# Let's compute the trace and determinant relationships
# Actually, let's try a Franklin-Reiter style attack

# The structure is:
# a0 = m
# a1 = m + u where u = 3p + 7q
# a2 = m + v where v = 11p + 13q  
# a3 = m + w where w = 17p + 19q

# From u and v: 13u - 7v = 13(3p+7q) - 7(11p+13q) = 39p + 91q - 77p - 91q = -38p
# So: p = -(13u - 7v) / 38

# Similarly: 11v - 13u = 11(11p+13q) - 13(3p+7q) = 121p + 143q - 39p - 91q = 82p + 52q = 2(41p + 26q)
# And: 19u - 7w = 19(3p+7q) - 7(17p+19q) = 57p + 133q - 119p - 133q = -62p
# So: p = -(19u - 7w) / 62

# The problem is we don't have u, v, w directly, we have the encrypted matrix

# Let me try a different approach: Franklin-Reiter on the matrix elements
# If we can express the ciphertext elements in terms of m, we might be able to use resultants

print("[*] Trying to factor n using algebraic relationships...")
print("[*] This may take a while...")

# Actually, let's think about this more carefully
# The quaternion (a0, a1, a2, a3) = (m, m+u, m+v, m+w)
# When we raise this to power e, we get some polynomial in m, u, v, w

# But we know u, v, w are linear in p, q
# So if we can find any relationship that eliminates m, we can factor n

# Let's try computing various combinations and taking GCDs
c0, c1, c2, c3 = ciphertext

# Try many different linear combinations
print("[*] Attempting systematic GCD search...")
found = False

# Extended search with more coefficients
for a in range(-10, 11):
    if a == 0:
        continue
    for b in range(-10, 11):
        if b == 0:
            continue
        for c in range(-10, 11):
            if c == 0:
                continue
            
            # Try combination: a*c1 + b*c2 + c*c3
            combo = (a*c1 + b*c2 + c*c3) % n
            g = GCD(combo, n)
            
            if 1 < g < n:
                if n % g == 0:
                    q = g
                    p = n // q
                    print(f"[+] Found factors using GCD({a}*c1 + {b}*c2 + {c}*c3, n)")
                    print(f"[+] p has {len(bin(p))-2} bits")
                    print(f"[+] q has {len(bin(q))-2} bits")
                    found = True
                    break
        if found:
            break
    if found:
        break
    if a % 5 == 0:
        print(f"[*] Progress: {a+10}/21 coefficient sets tested...")

if not found:
    print("[-] Extended GCD search failed")
    print("[*] The challenge might require a different approach")
    print("[*] Possible next steps:")
    print("    1. Implement Coppersmith's method")
    print("    2. Use lattice reduction")
    print("    3. Analyze the quaternion algebra structure more deeply")
    sys.exit(1)

# Decrypt
print("\n[*] Factorization successful! Proceeding to decrypt...")
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

# Implement quaternion arithmetic for decryption
def quat_mult_mod(q1, q2, mod):
    """Multiply two quaternions using Hamilton product"""
    a0, a1, a2, a3 = q1
    b0, b1, b2, b3 = q2
    
    c0 = (a0*b0 - a1*b1 - a2*b2 - a3*b3) % mod
    c1 = (a0*b1 + a1*b0 + a2*b3 - a3*b2) % mod
    c2 = (a0*b2 - a1*b3 + a2*b0 + a3*b1) % mod
    c3 = (a0*b3 + a1*b2 - a2*b1 + a3*b0) % mod
    
    return (c0, c1, c2, c3)

def quat_pow_mod(q, exp, mod):
    """Raise quaternion to power exp modulo mod"""
    result = (1, 0, 0, 0)
    base = q
    
    while exp > 0:
        if exp % 2 == 1:
            result = quat_mult_mod(result, base, mod)
        base = quat_mult_mod(base, base, mod)
        exp //= 2
    
    return result

# Decrypt modulo p and q separately
print("[*] Decrypting modulo p...")
cp = tuple(x % p for x in ciphertext)
dp = d % (p - 1)
mp_quat = quat_pow_mod(cp, dp, p)

print("[*] Decrypting modulo q...")
cq = tuple(x % q for x in ciphertext)
dq = d % (q - 1)
mq_quat = quat_pow_mod(cq, dq, q)

# CRT to combine
print("[*] Combining results with CRT...")
def crt(a, b, m1, m2):
    M = m1 * m2
    M1 = M // m1
    M2 = M // m2
    y1 = inverse(M1, m1)
    y2 = inverse(M2, m2)
    return (a * M1 * y1 + b * M2 * y2) % M

m_quat = tuple(crt(mp_quat[i], mq_quat[i], p, q) for i in range(4))

# The first component is m
m = m_quat[0]
flag = long_to_bytes(m)

print(f"\n[+] Decrypted message: {flag}")
print(f"[+] FLAG: {flag.decode()}")
