from Crypto.Util.number import long_to_bytes, isPrime
from gmpy2 import invert
from collections import deque

n = 44451185192213142526148486146224917510299587299799274190427685743486430985943994626332941446986394683065927937983014043430122283881545633401349754081716499086383386114183928509153604480972366256580593863806880714378086576833896541200363842949505721939341019320217861628563544604362769330469029272073437144251768484663527344161041789182045101043560092049490923260637173077825358028514203931872982751196873762522578569458976996705526569195272020911017933595800148064042688254240044798365612625807124572228502899959
c = 15059699900490583290879480458389742314140903373891090649599535027011362256088900972447091712889490005564113045861641599413534742376657700013519605958948942157369538971828980770456879033422947654562622686268914156774323063547501784806725283010437505154859978134333535500790421379792188182278205629223380053944531027913931101737661584830942566510260466649362745584954588040393189265460871322843300514814399730683057956428641247922601807578460342695489120554466476799018610800735239470574603264456237715819459056073
e = 65537

# BFS approach - keep all valid candidates at each position
# Start with p=7, q=7 (both end with 7)
candidates = [(7, 7)]

for pos in range(1, 257):
    mod = 10 ** (pos + 1)
    new_candidates = []
    
    for p, q in candidates:
        for p_digit in [6, 7]:
            for q_digit in [6, 7]:
                test_p = p_digit * (10 ** pos) + p
                test_q = q_digit * (10 ** pos) + q
                
                # Check if the last (pos+1) digits match using modular arithmetic
                if (test_p * test_q) % mod == n % mod:
                    new_candidates.append((test_p, test_q))
                    
                    # Check if we found the complete factorization
                    if test_p * test_q == n:
                        print(f"Found p and q at position {pos}!")
                        print(f"p = {test_p}")
                        print(f"q = {test_q}")
                        print(f"p * q = {test_p * test_q}")
                        print(f"Match: {test_p * test_q == n}")
                        print(f"p is prime: {isPrime(test_p)}")
                        print(f"q is prime: {isPrime(test_q)}")
                        print(f"p digits: {set(str(test_p))}")
                        print(f"q digits: {set(str(test_q))}")
                        
                        # Decrypt
                        phi = (test_p - 1) * (test_q - 1)
                        d = invert(e, phi)
                        m = pow(c, d, n)
                        flag = long_to_bytes(m)
                        
                        print(f"\nFlag: {flag.decode()}")
                        exit(0)
    
    if not new_candidates:
        print(f"No candidates found at position {pos}")
        print(f"Previous candidates: {len(candidates)}")
        break
    
    candidates = new_candidates
    print(f"Position {pos}: {len(candidates)} candidates")
    
    # Prune if too many candidates (shouldn't happen with this constraint)
    if len(candidates) > 100:
        print(f"Warning: Too many candidates ({len(candidates)}), pruning...")
        candidates = candidates[:100]

print("Failed to find factorization")
