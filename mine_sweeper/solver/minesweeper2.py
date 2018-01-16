#!/usr/bin/env python3
import sys
import itertools
from datetime import datetime
from mine_field import mf, r

def open(r, c):
    if RESULT[r][c] == 'x':
        print("error! can't open: {} {}".format(r, c), file=sys.stderr)
        sys.exit(1)
    return int(RESULT[r][c])

# END ANSWER PREP
# BEGIN ACTUAL SOLUTION
neig = lambda c: {(c[0]+i,c[1]+j) for i in (1,0,-1) for j in (1,0,-1)}-{c}
def solve_mine(map, n):
    # Convert map to dict format : {(i,j): val}
    map  = [r.split() for r in map.split('\n')]
    a, b = len(map),len(map[0])
    map  = {(i,j): map[i][j] for i in range(a) for j in range(b)}

    size_q = a*b+1
    q = {i for i in map if map[i]=='?'} # cells with ?
    x = {i for i in map if map[i]=='x'} # cells with x
    e = {i:0 for i in map if map[i]=='0'} # empty cells (opened cells)
    while len(q) < size_q:
        # Set of constraints: (S, m) such that sum(S)=m
        C = {(frozenset(neig(i)&q), e[i]-len(neig(i)&x)) for i in e if neig(i)&q}
        if len(C) < 12: # <<Optimize this number>>
            C.add((frozenset(q), n-len(x)))
        size_C = -1
        while size_C<len(C)<220: # <<Optimize this number>>
            size_C = len(C)
            C.update({(S2-S1, m2-m1) for S1,m1 in C for S2,m2 in C if S2-S1 and (len(S2-S1)==m2-m1 or S1<=S2)})

        for S,m in C:
            if m == 0: # Open every cell in S since sum(S)=0
                for t in S:
                    map[t]=open(*t)
            if m == len(S): # Put x to every cell in S since sum(S)=|S|
                for t in S:
                    map[t]='x'
        # Update
        size_q = len(q)
        q = {i for i in map if map[i]=='?'} # cells with ?
        x = {i for i in map if map[i]=='x'} # cells with x
        e = {i: int(map[i]) for i in map.keys()-(q|x)} # empty cells (opened cells)

    if len(x)==n:
        return '\n'.join(' '.join(str(map[(i,j)]) for j in range(b)) for i in range(a))
    return '?'

def run_testing_suite():
    """
    runs mine solver on all tests from mine_field.py
    """
    global RESULT
    for i in range(len(mf)):
        mine_field, RESULT = mf[i], r[i]
        N = RESULT.count('x')
        RESULT = RESULT.split('\n')
        for x in range(len(RESULT)):
            RESULT[x] = RESULT[x].split(' ')
        print('beginning to solve new mine field # {}...'.format(i))
        print('UNSOLVED Mine Field:')
        print("{}".format(mine_field))
        starttime = datetime.now()
        answer = solve_mine(mine_field, N)
        endtime = datetime.now()
        print('time to solve... {}'.format(endtime - starttime))
        print('SOLVED Mine Field:')
        print('Mine Field Requires Guesses' if answer == '?' else answer)

if __name__ == "__main__":
    """
    MAIN APP, calls solve_mine
    """
    run_testing_suite()
