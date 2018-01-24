#!/usr/bin/env python3
SOLUTION = [
    [5, 4, 5, 4, 5, 4, 5, 6],
    [4, 3, 4, 3, 4, 5, 4, 5],
    [3, 4, 3, 4, 3, 4, 5, 4],
    [2, 3, 2, 3, 4, 3, 4, 5],
    [3, 2, 3, 2, 3, 4, 3, 4],
    [2, 1, 4, 3, 2, 3, 4, 5],
    [3, 2, 1, 2, 3, 4, 3, 4],
    [0, 3, 2, 3, 2, 3, 4, 5]
]
R = {x: i for i, x in enumerate('87654321')}
C = {x: i for i, x in enumerate('abcdefgh')}


def knight(p1, p2):
    a = [R[p1[1]], C[p1[0]]]
    b = [R[p2[1]], C[p2[0]]]
    print(p1, p2, a, b)
    if a[0] > b[0]:   pass
    elif b[0] > a[0]: a, b = b, a
    elif a[1] < b[1]: pass
    elif b[1] < a[1]: a, b = b, a
    else: return 0
    if a[1] > b[1]:
        a[0], b[0] = b[0], a[0]
        a, b = b, a
    b[0] += 7 - a[0]
    b[1] -= a[1]
    print('modified: ', a, b)
    return SOLUTION[b[0]][b[1]]

def main_app():
    a = [
        ['a1', 'c1', 2], ['a1', 'f1', 3], ['a1', 'f3', 3], ['a1', 'f4', 4], ['a1', 'f7', 5],
        ['a1', 'h8', 6], ['c3', 'h4', 4], ['c3', 'a1', 4], ['b7', 'a8', 4], ['e8', 'e1', 5],
        ['h6', 'b7', 3], ['b7', 'a8', 4], ['g2', 'h1', 4]
    ]
    for x in a:
        z = knight(x[0], x[1])
        print('expected = {}, actual = {}'.format(x[2], z))

if __name__ == "__main__":
    main_app()
