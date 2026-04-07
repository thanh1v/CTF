from Crypto.Util.number import bytes_to_long as B, getPrime as G
import math as M
F=open("flag.txt").read()
while 1:
    try:
        s=int(input("size > ") )
        if s<=len(F)*40:
            p=G(s)
        elif s<=10000:
            p=256
        u=p*p
        x=F+"a"*(1+M.ceil(s/8))
        x=B(x.encode())
        x-=x%p
        y=pow(x,0x10001,u)
        print(len(bin(x//p))-2)       
        print(bin(x//p).count("1"))   
        print(y,0x10001,u)            
    except:
        print("invalid input")
        break
