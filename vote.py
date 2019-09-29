from large_power_mod import *
from prime_finder import *
from mod_tester import *
from random import randint

# Large (safe) prime p
#p = 11
p = 2903
#p = 11
# Large prime q s.t. q | p-1
q = 86028323
# Generator of subgroup of Zp -> Gq
g = 65537
# Secret key, shared among voting authorities
s = 51
h = 0

votes = []
messages = []

def init():
    global h
    # Public key, g^s
    h = comp_large(g, s, q)
    
    print('Initial conditions of the system:')
    print('p: {}'.format(p))
    print('q: {}'.format(q))
    print('g: {}'.format(g))
    print('h: {}'.format(h))

def get_voter_input():
    print('\n#### VOTER {} ####'.format(len(votes)+1))
    #print('Enter priv value a:')
    #a = int(input())
    a = randint(1,int(0xFFFFFFFF))
    print('Your randomly generated key is {}'.format(hex(a)[2:].upper()))
    m0 = int(input('Enter your vote | -1 for Candidate A and 1 for Candidate B: '))
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

def main():
    init()
    votes.append(get_voter_input())
    votes.append(get_voter_input())
    votes.append(get_voter_input())
    votes.append(get_voter_input())
    votes.append(get_voter_input())

    print('\n\n#### PUBLIC BULLETIN BOARD ####')
    for v in votes:
        print('Voter {} cypher pair: ({},{})'.format(v[0],v[1],v[2]))
    X,Y = mult_votes(votes)
    print('#### Multiplicative Cypher: ({},{})\n'.format(X,Y))
    print('Decrypting public cypher...')
    res = dec(q,s,X,Y)
    print('Done.  Decrypted vote total: {}'.format(hex(int(res))[2:].upper()))
    print('----------')
    print('Checking discrete logarithms of possible outcomes...')
    t = find_tally(res)
    print('Done!')
    win = 'A' if t < 0 else 'B'
    print('Candidate {} wins by {} votes!!!'.format(win,abs(t)))
    #print('Result should be {}'.format(smsg(messages)))


if __name__=='__main__':
    main()
