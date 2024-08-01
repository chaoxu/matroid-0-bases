from z3 import *
from itertools import combinations, product

# test if Z_2xZ_2 is strongly isolating for block matroid of rank 3

r = 3
n = 2*r
E = frozenset(range(n))
E_choose_r = [frozenset(X) for X in list(combinations(E, r))]

# isolated block
B = frozenset(range(r))

def exchange(X,x,y):
    return (X-frozenset([x]))|frozenset([y])

s = Solver()

# boolean variable indicates a base
base = dict()
for X in E_choose_r:
    base[X] = Bool(str(X))

# variable for label of each element
label = dict()
for x in E:
    label[(x,0)] = Int(str(x)+"_0")
    label[(x,1)] = Int(str(x)+"_0")
    s.add(label[(x,0)]<=1)
    s.add(label[(x,0)]>=0)
    s.add(label[(x,1)]<=1)
    s.add(label[(x,1)]>=0)

# B is a block, hence a block matroid
s.add(And(base[B],base[E-B]))

# matroid constraint: for base X, Y and x in X-Y, there is y in Y-X s.t. X-x+y is a base
for X in E_choose_r:
    for Y in E_choose_r:
        for x in X-Y:
            s.add(Implies(And(base[X],base[Y]),Or(*[base[exchange(X,x,y)] for y in Y-X])))

# block constraints: X and E-X are bases, then l(X) != l(B)
for X in E_choose_r:
    if X!=B:
        s.add(Implies(And(base[X],base[E-X]),Or(Sum([label[(x,0)] for x in X])%2 != Sum([label[(x,0)] for x in B])%2),Sum([label[(x,1)] for x in X])%2 != Sum([label[(x,1)] for x in B])%2))

# check if satisfiable
if s.check()==sat:
    print(s.model())
else:
    print("Z_2xZ_2 is not strongly isolating for block matroid of rank 3")
