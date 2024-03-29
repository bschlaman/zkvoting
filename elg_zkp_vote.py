from random import randint

# Helpful funcitons
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
    return int(a/b)%n

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

# INITIAL CONDITIONS
# Large (safe) prime p
# p = 2903
# Large prime q s.t. q | p-1
q = 86028323
# Generator of subgroup of Zp -> Gq
g = 65537
# Secret key, shared among voting authorities
s = 932231
h = 0

votes = []
messages = []

def init():
    global h
    # Public key, g^s
    h = comp_large(g, s, q)
    
    print('\nInitial conditions of the system:')
    #print('p: {}'.format(p))
    print('\nq is a large prime chosen by the voting authorities.  It is often a \"safe\" prime, meaning that (q-1)/k is also prime, in order to prevent small-subgroup-attacks.  This value is PUBLIC.\n')
    print('q: {}'.format(q))
    print('\ng is a generator of q chosen by the voting authorities.  This means that any value {0,...,q-1} is the outcome of g^x (mod q) for some x.  This value is PUBLIC.\n')
    print('g: {}'.format(g))
    print('\nh is a public key generated by g^s (mod q) for some secret key s.  h is used to encrypt votes such that only the voting authorities can decrypt it.  Pieces of the secret key are shared among multiple voting authorities.  In our case, it is {}.  s is PRIVATE but h is PUBLIC.\n'.format(hex(s)[2:].upper()))
    print('h: {}'.format(hex(h)[2:].upper()))

def get_voter_input():
    print('\n#### VOTER {} ####'.format(len(votes)+1))
    #print('Enter priv value a:')
    #a = int(input())
    a = randint(1,int(0xFFFFFFFF))
    print('Your randomly generated key is {}'.format(hex(a)[2:].upper()))
    m0 = int(input('Enter your vote | \"-1\" for Candidate A and \"1\" for Candidate B: '))
    messages.append(m0)
    #m = comp_large(g,m0,q)
    if m0 == -1:
        # "1" is dummy value since m not used in calculation of x
        x = enc(q,g,s,a,1)[0]
        y = frac_large(comp_large(h,a,q),g,q)
    elif m0 == 1:
        m = comp_large(g,m0,q)
        x,y = enc(q,g,s,a,m)
    else:
        exit(1)
    print('Your cyphertext pair is ({},{})'.format(x,y))
    return len(votes)+1,x,y

def mult_votes(v):
    c1=c2=1
    for x in v:
        c1 = (c1 * x[1]) % q
        c2 = (c2 * x[2]) % q
    return c1,c2

def smsg(m):
    tot = 0
    for x in m:
        tot += x
    return tot

def find_tally(res):
    for x in range(0,len(votes)+1):
        if comp_large(g,x,q) == res:
            #print(x)
            return x
        if frac_large(1,comp_large(g,abs(x),q),q) == res:
            #print('minus',x)
            return -x

def menu(opts):
    for item in enumerate(opts):
        s = '{}) {}'.format(str(item[0]+1), item[1])
        print(s)
    print('{}) I\'m convinced!  I\'ll cast my real vote now.'.format(len(opts)+1))
    c = int(input('Select option: '))
    return c-1

def zkp_voter():
    print('\n#### VOTER {} ZKP MACHINE TEST ####'.format(len(votes)+1))
    print('You have been selected to use ZKP to test that the machine is indeed giving proper encryptions, and not some random value (or the wrong vote)!'+'\nYou just voted 5 times to get 5 cypher-texts, or \"receipts\".  Now randomly choose some for the machine to decrypt.  That will render these votes invalid, but the machine\'s integrity will be verified.')
    print('Generating votes and cyphers...')

    my_receipts = []
    for x in range(0, 5):
        a = randint(1,int(0xFFFFFFFF))
        vote = 'Cand A' if randint(0,1) == 0 else 'Cand B'
        if vote.endswith('A'):
            # "1" is dummy value since m not used in calculation of x
            x = enc(q,g,s,a,1)[0]
            y = frac_large(comp_large(h,a,q),g,q)
        elif vote.endswith('B'):
            m = comp_large(g,1,q)
            x,y = enc(q,g,s,a,m)
        my_receipts.append((vote,x,y))
    print('\nDone!  Choose one of your receipts to feed back into the machine to decrypt.  NOTE: you can see the \'Cand A\' or \'Cand B\', but the computer cannot!\n')
    c = 0
    proof = 0
    while True:
        c = menu(my_receipts)
        if c == len(my_receipts):
            break
        print('\nDecrypting {}...'.format(my_receipts[c]))
        d = dec(q,s,my_receipts[c][1],my_receipts[c][2])
        cand = 'B' if d == comp_large(g,1,q) else 'A'
        print('%%%%%%%%%% Machine says: This vote would have been for candidate {}'.format(cand))
        proof+=1
        cert = 1-pow(2,-1*proof)
        print('You can now be {}% sure that this machine gives honest encryptions.\n'.format(round(100*cert,5)))

def main():
    init()

    print('\nNow it\'s time to act as the voters.  There are 5 voters in our system.  Each voter generates a random private key (in our case, the computer does it for them).  They then encrpt their vote using their private key and the voting authority public key using ElGamal encryption.  KEY CONCEPT: This encrpytion scheme is multiplicatively homomorphic; that is, ENC(v1) * ENC(v2) * ENC(v3) * ... = ENC(v1 + v2 + v3 + ...), which makes it exellent for tallying.  Now go vote!\n\n')

    votes.append(get_voter_input())
    votes.append(get_voter_input())
    votes.append(get_voter_input())
    votes.append(get_voter_input())
    zkp_voter()
    votes.append(get_voter_input())

    print('\n\n#### PUBLIC BULLETIN BOARD ####')
    for v in votes:
        print('Voter {} cypher pair: ({},{})'.format(v[0],v[1],v[2]))
    X,Y = mult_votes(votes)
    print('#### Multiplicative Cypher: ({},{})\n'.format(X,Y))
    print('Decrypting public cypher...')
    res = dec(q,s,X,Y)
    print('Done.  Decrypted vote total: {}'.format(hex(int(res))[2:].upper()))
    print('----------------------------------------------------')
    print('Checking discrete logarithms of possible outcomes...')
    t = find_tally(res)
    print('Done!')
    win = 'A' if t < 0 else 'B'
    print('Candidate {} wins by {} votes!!!'.format(win,abs(t)))
    #print('Result should be {}'.format(smsg(messages)))

if __name__=='__main__':
    main()
