def get_powers(x):
    powers = []
    i = 1
    while i <= x:
        if i & x:
            powers.append(i)
        i <<= 1
    return powers

def main():
    print('a^x mod p')
    a = int(input('a: '))
    x = int(input('x: '))
    p = int(input('p: '))
    print(str(a)+'^'+str(x)+' mod '+str(p))

    pws = get_powers(x)
    alp = {1:a%p}
    i = 2
    while i < pws[-1] + 1:
        alp[i] = pow(alp[i>>1],2) % p
        i <<= 1
    print(alp)

    total=1
    for pw in pws:
        total *= alp[pw]
    final = int(total%p)
    print(final)


def comp_large(a,x,p):
    alp = {1:a%p}
    total = 1 if not 1 & x else alp[1]
    i = 2
    while i <= x:
        alp[i] = pow(alp[i>>1],2) % p
        if i & x:
            total = (total * alp[i]) % p
        i <<= 1
    return total % p

def frac_large(a,b,n):
    while a%b != 0:
        factor = 1
        while b * factor < n:
            factor += 1
        a = (a * factor) % n
        b = (b * factor) % n
    return (a/b)%n


if __name__=='__main__':
    main()
