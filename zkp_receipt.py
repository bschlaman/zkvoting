from elg_zkp_vote import *

def menu(opts):
    for item in enumerate(opts):
        s = '{}) {}'.format(str(item[0]+1), item[1])
        print(s)
    print('{}) I\'m convinced!  I\'ll cast my real vote now.'.format(len(opts)+1))
    c = int(input('Select option: '))
    return c-1

def zkp_voter():
    my_receipts = []
    
    for x in range(0, 5):
        vote = 'A' if randint(0,1) == 0 else 'B'
        my_receipts.append((vote,randint(1,1000),randint(1,1000)))
    
    print('\nChoose one of your receipts to feed back into the machine to decrypt.  NOTE: you can see the \'A\' or \'B\', but the computer cannot!\n')
    c = 0
    proof = 0
    while True:
        c = menu(my_receipts)
        if c == len(my_receipts):
            break
        print('\nDecrypting {}'.format(my_receipts[c]))
        print('Machine says: This vote would have been for candidate {}'.format(my_receipts[c][0]))
        proof+=1
        cert = 1-pow(2,-1*proof)
        print('You can now be {}% sure that this machine gives honest encryptions.\n'.format(round(100*cert,5)))

if __name__=='__main__':
    zkp_voter()
