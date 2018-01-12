#!/usr/bin/env python3

def ship_size(row, i):
    size = 0
    if 0 <= i < 10 and row[i] == 1:
        row[i] = 0
        size += 1 + ship_size(row, i + 1) + ship_size(row, i - 1)
    return size

def check_diagonals(f):
    coords = {}
    for r in range(10):
        for c in range(10):
            coords[(r, c)] = f[r][c]
    for coord, val in coords.items():
        if val == 1:
            r, c = coord[0], coord[1]
            diagonals = [
                coords.get((r - 1, c - 1), 0), coords.get((r - 1, c + 1), 0),
                coords.get((r + 1, c - 1), 0), coords.get((r + 1, c + 1), 0)
            ]
            if any(diagonals): return False
    return True

def validateBattlefield(f):
    if check_diagonals(f) is False: return False
    fr = list(zip(*f[::-1]))
    for r in range(10): fr[r] = list(fr[r])

    ships, subs = [4, 3, 3, 2, 2, 2], 4
    while len(ships) > 0:
        pre_ships = len(ships) + subs
        r = 0
        while r < 10:
            c = 0
            while c < 10:
                if f[r][c] == 1:
                    c_r, c_c = c, 9 - r
                    count_r = ship_size(f[r].copy(), c)
                    count_c = ship_size(fr[c_r].copy(), c_c)
                    count = max(count_r, count_c)
                    if count_r > 1 and count_c > 1: return False
                    if count_r == 1 and count_c == 1:
                        subs -= 1
                        ship_size(f[r], c)
                        ship_size(fr[c_r], c_c)
                    if len(ships) > 0  and count == ships[0]:
                        if len(ships) > 0: del ships[0]
                        else: return False
                        ship_size(f[r], c)
                        ship_size(fr[c_r], c_c)
                c += 1
            r += 1
        if pre_ships == len(ships) + subs: return False
    if len(ships) == 0 and subs == 0: return True
    return False

battleField = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

battleField2 = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

battleField3 = [
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
valid = validateBattlefield(battleField3)
print(valid)
