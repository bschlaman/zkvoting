from large_power_mod import *
from prime_finder import *

def coprime(a,b):
    return gcd(a,b)==1

def single_g(g):    
    print('g = '+str(g))
    for a in range(0,n):
        res = pow(g,a) % n
        #print('a='+str(a)+' '+'(g^a)mod7='+str(res))
        print('('+str(g)+'^'+str(a)+')mod7 = '+str(res))

def contains_all(res,m):
    for x in range(1,m):
        if x not in res:
            return False
    return True

def generator_test(n):
    print('(g^a) mod '+str(n))
    for g in range(0,n):
        outputs = []
        for a in range(0,n):
            res = comp_large(g,a,n)
            outputs.append(res)
        #print(str(g)+': ' + str(contains_all(outputs,n)))
        if contains_all(outputs,n):
            print(g)

def is_generator(a,p):
    print('('+str(a)+'^x) mod '+str(p))
    outputs = []
    for x in range(0,p):
        res = comp_large(a,x,p)
        outputs.append(res)
    return contains_all(outputs,p)

def ones_counter(n):
    for x in range(0,n):
        ones = 0
        for y in range(0,n):
                if(comp_large(x,y,n)==1):
                        ones+=1
        print(x,ones)

def cycle_length(g,n):
    cl = 1
    while comp_large(g,cl,n) != 1 and cl < n:
        cl+=1
    if cl==n:
        return -1
    else:
        return cl

def cycle_lengths(n):
    for x in range(1,n):
        print(x,cycle_length(x,n))

def cycle_generator(n):
    for x in range(1,n):
        cycl = cycle_length(x,n)
        s = ' '*(3-len(str(x))) + str(x) + ':' + ' '*(3-len(str(cycl))) + '#' + str(cycl) + '| 1'
        for y in range(1,n):
            res = comp_large(x,y,n)
            s += ' '*(3-len(str(res))) + str(res)
            if res == 1:
                break
        print(s)

def enc(p,g,s,alph,m):
    pubk = comp_large(g,s,p)
    x = comp_large(g,alph,p)
    y = comp_large(pubk,alph,p) * m % p
    #print('x: {}\ny: {}'.format(x,y))
    return x,y

def dec(p,s,x,y):
    num = y
    den = comp_large(x,s,p)
    res = frac_large(num,den,p)
    #print(res)
    return res

def exp_test():
    print('(g^a * g^b)mod p = g^((a+b)mod p-1)')
    g = int(input('Enter g: '))
    a = int(input('Enter a: '))
    b = int(input('Enter b: '))
    p = int(input('Enter p: '))
    print('('+str(g)+'^'+str(a)+' * '+str(g)+'^'+str(b)+')mod '+str(p)+' = '+str(pow(g,a)*pow(g,b)%p))
    print('('+str(g)+'^(('+str(a)+'+'+str(b)+')mod '+str(p-1)+')mod '+str(p)+' = '+str(pow(g,(a+b)%(p-1))%p))
