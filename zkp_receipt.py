from random import shuffle
from elg_zkp_vote import *

my_receipts = []

for x in range(0, 5):
    vote = 'A' if randint(0,1) == 0 else 'B'
    my_receipts.append((vote,randint(1,1000),randint(1,1000)))

print(my_receipts)
shuffle(my_receipts)
print(my_receipts)
