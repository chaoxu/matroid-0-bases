from z3 import *
from itertools import combinations, product

# test if Z_m is strongly m-1 close
m = 4

r = m
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
    label[x] = Int(str(x))
    s.add(label[x]<=m-1)
    s.add(label[x]>=0)

# B is a block, hence a block matroid
s.add(And(base[B],base[E-B]))

# matroid constraint: for base X, Y and x in X-Y, there is y in Y-X s.t. X-x+y is a base
for X in E_choose_r:
    for Y in E_choose_r:
        for x in X-Y:
            s.add(Implies(And(base[X],base[Y]),Or(*[base[exchange(X,x,y)] for y in Y-X])))

# block constraints: X and E-X are bases, then l(X)%m != l(B)%m
for X in E_choose_r:
    if X!=B:
        s.add(Implies(And(base[X],base[E-X]),Sum([label[x] for x in X])%m != Sum([label[x] for x in B])%m))

# check if satisfiable
if s.check()==sat:
    print(s.model())
else:
    print("Z_"+str(m)+" is strongly "+str(m-1)+"-close")
