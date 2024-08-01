from itertools import combinations
from sage.matroids.advanced import *

r = 6
n = 2*r
E = frozenset(range(n))
E_choose_r = [frozenset(X) for X in list(combinations(E, r))]

def settype(S):
    v1 = 1 if 0 in S else 0
    v2 = 1 if 11 in S else 0
    v3 = len(S & frozenset([1,2,3,4,5]))
    v4 = len([x for x in S & frozenset([1,2,3,4,5]) if x+5 in S])
    return (v1,v2,v3,v4)

basetypes = [(0,0,x,1) for x in [1,2,3,4,5]] \
            +[(1,0,x,0) for x in [0,2,4,5]] \
            +[(1,0,x,1) for x in [1,2,3,4]] \
            +[(0,1,x,0) for x in [0,1,2,3,4,5]] \
            +[(1,1,x,0) for x in [0,1,2,3,4]]

bases = [X for X in E_choose_r if settype(X) in basetypes]

M = BasisMatroid(groundset=E,bases=bases)

# assign labeling
label = {0:3, 1:2, 2:2, 3:2, 4:2, 5:2, 6:5, 7:5, 8:5, 9:5, 10:5, 11:4}

blocks = []
for B in bases:
    if E-B in bases:
        blocks.append(B)

# check if M is a matroid
print(M.is_valid())

# show the type non-blocks
print(frozenset([settype(X) for X in bases]) - frozenset([settype(X) for X in blocks]))

# show {0,1,2,3,4,5} is the only block with label sum 1
for X in blocks:
    if sum([label[x] for x in X])%6==1:
        print(X)
