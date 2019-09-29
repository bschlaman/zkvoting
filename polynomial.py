
from large_power_mod import comp_large
from random import randint

a = 22
p = 86028157

scalars = []
def genpoly(deg):
    global scalars
    polystr = ''
    scalars = []
    for x in range(0,deg):
        scalars.append(randint(0,500))
        #sign = ' - ' if scalars[x] < 0 else ' + '
        sign = ' + ' if x else ''
        term = 'x^' + str(x)
        polystr += sign + str(abs(scalars[x])) + term
    print(polystr)

def evpoly(p):
    res = 0
    for x in enumerate(scalars):
        res += x[1] * pow(p,x[0])
    return res

hidings = []
def comp_hidings(x):
    global hidings
    # using len(scalars) simply to get degree
    for deg in range(0,len(scalars)):
        hidings.append(comp_large(a,pow(x,deg),p))
    print(hidings)

def calc_res(hidings):
    res = 1
    for x in enumerate(hidings):
        res *= pow(x[1], scalars[x[0]])
    return res % p

