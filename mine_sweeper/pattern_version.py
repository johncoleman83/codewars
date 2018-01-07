#!/usr/bin/env python3
import sys
import itertools
from mine_field import mine_field, RESULT


def open(r, c):
    if RESULT[r][c] == 'x':
        print("error! can't open: {} {}".format(r, c), file=sys.stderr)
        sys.exit(1)
    return int(RESULT[r][c])


# END ANSWER PREP
# BEGIN ACTUAL SOLUTION


class MineSweeper():
    def __init__(self, mine_field, bombs):
        self.bombs = bombs
        if type(mine_field).__name__ == 'str':
            self.mf = mine_field.split('\n')
            for x in range(len(self.mf)):
                self.mf[x] = self.mf[x].split(' ')
        else:
            self.mf = mine_field
        self.ROWS = len(self.mf)
        self.COLS = len(self.mf[0])
        self.borders = {}
        self.clusters = {}
        self.unknown = set()

    def generate_border_spaces(self, r, c, idx):
        """
        this containes all border spaces if on the board
        """
        self.borders[idx] = [True]
        if r > 0:
            self.borders[idx].append([r - 1, c])
        if r > 0 and c < self.COLS - 1:
            self.borders[idx].append([r - 1, c + 1])
        if r > 0 and c > 0:
            self.borders[idx].append([r - 1, c - 1])
        if c < self.COLS - 1:
            self.borders[idx].append([r, c + 1])
        if c > 0:
            self.borders[idx].append([r, c - 1])
        if r < self.ROWS - 1:
            self.borders[idx].append([r + 1, c])
        if r < self.ROWS - 1 and c < self.COLS - 1:
            self.borders[idx].append([r + 1, c + 1])
        if r < self.ROWS - 1 and c > 0:
            self.borders[idx].append([r + 1, c - 1])

    def complete_border_neighbors(self):
        """
        completes generation of border neighbors
        """
        i = 0
        needed = list(
            set(range(0, self.ROWS * self.COLS)) - set(self.borders.keys())
        )
        while i < len(needed):
            idx = needed[i]
            r = idx // self.COLS
            c = idx - (r * self.COLS)
            self.generate_border_spaces(r, c, idx)
            i += 1

    def find_neighbors(self, idx, char, test=False):
        """
        finds neighboring spaces of givin input character
        """
        coords = []
        if char == '?' and self.borders[idx][0] is False:
            return []
        for space in self.borders[idx][1:]:
            if char == 'int' == type(self.mf[space[0]][space[1]]).__name__:
                coords.append(space)
            elif self.mf[space[0]][space[1]] == char:
                coords.append(space)
        if char == '?' and len(coords) == 0 and test is False:
            self.borders[idx][0] = False
        elif char == '?':
            coords.sort()
        return coords

    def open_list(self, coords, final=False):
        """
        CALLS OPEN BASED ON INPUT LIST
        """
        for coord in coords:
            idx = coord[0] * self.COLS + coord[1]
            if idx in self.unknown:
                self.unknown.remove(idx)
            revealed = open(coord[0], coord[1])
            if type(revealed).__name__ == 'str':
                revealed = int(revealed)
            self.mf[coord[0]][coord[1]] = revealed

    def mark_bombs(self, coords):
        """
        Marks Bombs on input field from input coords
        """
        for coord in coords:
            idx = coord[0] * self.COLS + coord[1]
            if idx in self.unknown:
                self.unknown.remove(idx)
            self.mf[coord[0]][coord[1]] = 'x'

    def initial_board_scan(self):
        """
        Reveals Board based on revealed spaces logic
        """
        r = 0
        while r < self.ROWS:
            c = 0
            while c < self.COLS:
                square = self.mf[r][c]
                idx = r * self.COLS + c
                if idx not in self.borders:
                    self.generate_border_spaces(r, c, idx)
                if square == 'x' or square == '?':
                    self.unknown.add(idx)
                    c += 1
                    continue
                if type(square).__name__ == 'str' and square.isdigit():
                    square = int(square)
                    self.mf[r][c] = square
                unknown = self.find_neighbors(idx, '?')
                if len(unknown) == 0:
                    c += 1
                    continue
                bombs = self.find_neighbors(idx, 'x')
                if self.mf[r][c] == '0' or self.mf[r][c] == 0:
                    self.open_list(unknown)
                elif len(bombs) == square:
                    self.open_list(unknown)
                elif square - len(bombs) == len(unknown):
                    self.mark_bombs(unknown)
                    self.bombs -= len(unknown)
                else:
                    c += 1
                    continue
                nr, nc = unknown[0][0], unknown[0][1]
                if nr * self.COLS + nc < r * self.COLS + c:
                    r, c = nr, nc
                r = 0 if r == 0 else r - 1
            r += 1
        print('\n'.join([' '.join([str(x) for x in row]) for row in self.mf]))
        print()
        self.unknown = [
            [i // self.COLS, i - i // self.COLS * self.COLS] for i in self.unknown
        ]
        self.complete_border_neighbors()

    def scan_perimeter_pieces(self, perimeter):
        """
        scans for bombs
        """
        updates = 0
        for space in perimeter:
            r, c = space[0], space[1]
            square = self.mf[r][c]
            idx = r * self.COLS + c
            unknown = self.find_neighbors(idx, '?')
            bombs = self.find_neighbors(idx, 'x')
            if len(bombs) == square:
                updates += 1
                self.open_list(unknown)
            elif square - len(bombs) == len(unknown):
                updates += 1
                self.mark_bombs(unknown)
                self.bombs -= len(unknown)
        return updates

    def store_new_cluster(self, unknown):
        """
        STORES A CLUSTER OF '?' after discoverd
        """
        index = len(self.clusters)
        perimeter = set()
        for space in unknown:
            idx = space[0] * self.COLS + space[1]
            neighbors = self.find_neighbors(idx, 'int')
            for n in neighbors:
                idx = n[0] * self.COLS + n[1]
                perimeter.add(idx)
        perimeter = sorted(list(perimeter))
        for i in range(len(perimeter)):
            idx = perimeter[i]
            r = idx // self.COLS
            c = idx - (r * self.COLS)
            perimeter[i] = [r, c]
        return perimeter

    def valid_bomb_placement(self, perimeter, unknown):
        """
        DETERMINES IF PERIMETER IS VALID BASED ON BOMB PLACEMENTS
        """
        for space in perimeter:
            r, c = space[0], space[1]
            square = self.mf[r][c]
            idx = r * self.COLS + c
            unknown = self.find_neighbors(idx, '?', True)
            bombs = self.find_neighbors(idx, 'x')
            if len(bombs) != square:
                return False
        return True

    def clean_guesses(self, unknown, i, end):
        """
        cleans board of guesses, resets to '?'
        """
        numbers = []
        while i < end:
            r, c = unknown[i][0], unknown[i][1]
            if self.mf[r][c] != 'x':
                numbers.append([r, c])
            self.mf[r][c] = '?'
            i += 1
        return numbers

    def brute_force_combo_check(self, unknown, perimeter):
        all_guesses = []
        for combo in itertools.combinations(
            [x for x in range(len(unknown))], self.bombs
        ):
            guess_combo = []
            for i in combo:
                r, c = unknown[i][0], unknown[i][1]
                self.mf[r][c] = 'x'
                guess_combo.append([r, c])
            if self.valid_bomb_placement(perimeter, unknown) is True:
                numbers = self.clean_guesses(unknown, 0, len(unknown))
                all_guesses.append({
                    'bombs': guess_combo,
                    'numbers': numbers
                })
            else:
                self.clean_guesses(unknown, 0, len(unknown))
        return all_guesses

    def find_patterns_in_guesses(self, guesses):
        """
        Attempts to find all common bombs and numbers from all potential bomb patterns
        """
        common_n, common_b = {}, {}
        for guess in guesses:
            n, b = guess['numbers'], guess['bombs']
            nidx = [s[0] * self.COLS + s[1] for s in n]
            bidx = [s[0] * self.COLS + s[1] for s in b]
            if common_n == {}:
                common_n, common_b = set(nidx), set(bidx)
                continue
            common_n = common_n.intersection(set(nidx))
            common_b = common_b.intersection(set(bidx))
        common_n = [[i // self.COLS, i - i // self.COLS * self.COLS] for i in common_n]
        common_b = [[i // self.COLS, i - i // self.COLS * self.COLS] for i in common_b]
        if len(common_n) > 0:
            self.open_list(list(common_n))
        if len(common_b) > 0:
            self.mark_bombs(list(common_b))
            self.bombs -= len(common_b)
        return 1 if len(common_n) > 0  or len(common_b) > 0 else 0

    def do_handle_pattern(self, pattern, lower, lower_coords):
        pass

    def handle_consecutive_lines(self, r_line, c_line):
        updates = 0
        patterns = [
            '242', '345', '1222', '2331', '222', '2331', '13231', '2222'
        ]
        for line in r_line:
            upper, lower, upper_coords, lower_coords = [], [], [], []
            for space in line:
                r, c = space[0], space[1]
                if r > 0:
                    upper_coords.append([r - 1, c])
                    upper.append(self.mf[r - 1][c])
                if r < self.ROWS - 1:
                    lower_coords.append([r + 1, c])
                    lower.append(self.mf[r + 1][c])
            #l, u = ''.join([str(x) for x in lower]), ''.join([str(x) for x in uppper])
            s, e = 0, 1
            while e < len(upper):
                if upper[s:e + 1] == [1, 1]:
                    idxs = upper_coords[s][0] * self.COLS + upper_coords[s][1]
                    idxe = upper_coords[e][0] * self.COLS + upper_coords[e][1]
                    checks = self.find_neighbors(idxs, '?')
                    checke = self.find_neighbors(idxe, '?')
                    if len(checks) + len(checke) == 5 and abs(idxe - idxs) == 1:
                        updates += 1
                        if len(checks) == 3:
                            r, c = upper_coords[s][0] + 1, upper_coords[s][1] - 1
                            revealed = open(r, c)
                            self.mf[r][c] = revealed
                        if len(checke) == 3:
                            r, c = upper_coords[e][0] + 1, upper_coords[e][1] + 1
                            revealed = open(r, c)
                            self.mf[r][c] = revealed
                if (upper[s:e + 1] in [[1, 2], [2, 3], [2, 4]]
                    or upper[s:e + 1] in [[2, 1], [3, 2], [4, 2]]):
                    rs, cs = upper_coords[s][0], upper_coords[s][1]
                    idxs = upper_coords[s][0] * self.COLS + upper_coords[s][1]
                    re, ce = upper_coords[e][0], upper_coords[e][1]
                    idxe = upper_coords[e][0] * self.COLS + upper_coords[e][1]
                    checks = self.find_neighbors(idxs, '?')
                    checke = self.find_neighbors(idxe, '?')
                    if len(checks) + len(checke) <= 6 and abs(idxe - idxs) == 1:
                        updates += 1
                        if s != 0 and upper[s:e + 1] in [[2, 1], [3, 2], [4, 2]]:
                            r, c = upper_coords[s][0] + 1, upper_coords[s][1] - 1
                            self.mf[r][c], self.bombs = 'x', self.bombs - 1
                        elif e != len(upper) - 1 and upper[s:e + 1] in [[1, 2], [2, 3], [2, 4]]:
                            r, c = upper_coords[e][0] + 1, upper_coords[e][1] + 1
                            self.mf[r][c], self.bombs = 'x', self.bombs - 1
                        else:
                            updates -= 1
                s, e = s + 1, e + 1
        print('\n'.join([' '.join([str(x) for x in row]) for row in self.mf]))
        print()
        return updates


    def check_for_patterns(self, unknown):
        """
        searches for lines of unknown boxes
        """
        rows, cols, r_line, c_line = {}, {}, [], []
        for i in unknown:
            if i[0] not in rows:
                rows[i[0]] = []
            if i[1] not in cols:
                cols[i[1]] = []
            rows[i[0]].append(i.copy())
            cols[i[1]].append(i.copy())
        r_line = [sorted(l) for l in rows.values() if len(l) >= 3]
        c_line = [sorted(l) for l in cols.values() if len(l) >= 3]
        if len(r_line) + len(c_line) == 0:
            return 0
        i = 0
        while i < len(r_line):
            l = r_line[i]
            s, e = 0, 2
            consecutive = False
            while e < len(l):
                if abs(l[e][1] - l[s][1]) == 2:
                    consecutive = True
                    j = 2
                    while e < len(l) and abs(l[e][1] - l[s][1]) == j:
                        e, j = e + 1, j + 1
                    break
                else:
                    s, e = s + 1, e + 1
            if consecutive is False:
                del r_line[i]
            else:
                r_line[i] = r_line[i][s:e]
                i += 1
        i = 0
        while i < len(c_line):
            l = c_line[i]
            s, e = 0, 2
            consecutive = False
            while e < len(l):
                if abs(l[e][0] - l[s][0]) == 2:
                    consecutive = True
                    j = 2
                    while e < len(l) and abs(l[e][0] - l[s][0]) == j:
                        e, j = e + 1, j + 1
                    break
                else:
                    s, e = s + 1, e + 1
            if consecutive is False:
                del c_line[i]
            else:
                c_line[i] = c_line[i][s:e]
                i += 1
        if len(r_line) + len(c_line) == 0:
            return 0
        updates = self.handle_consecutive_lines(r_line, c_line)
        return updates


    def do_handle_unknowns(self, unknown):
        updates = 0
        perimeter = self.store_new_cluster(unknown)
        updates = self.check_for_patterns(unknown)
        if updates > 0:
            return True
        all_guesses = self.brute_force_combo_check(
            unknown, perimeter
        )
        if len(all_guesses) == 1:
            self.mark_bombs(all_guesses[0]['bombs'])
            self.bombs -= len(all_guesses[0]['bombs'])
            self.open_list(all_guesses[0]['numbers'])
            if self.bombs == 0:
                i = 0
                while i < len(unknown):
                    r, c = unknown[i][0], unknown[i][1]
                    if self.mf[r][c] != '?':
                        del unknown[i]
                    else:
                        i += 1
                self.open_list(unknown)
                updates -= 1
            updates += 1
        else:
            updates += self.find_patterns_in_guesses(all_guesses)
        updates += self.scan_perimeter_pieces(perimeter)
        return None if updates == 0 else True

    def find_unknown_spaces(self, unknown):
        """
        if unknown is None or len(unknown) == 0:
            unknown = []
            for r in range(self.ROWS):
                for c in range(self.COLS):
                    if self.mf[r][c] == '?':
                        unknown.append([r, c])
        else:
        """
        i = 0
        while i < len(unknown):
            r, c = unknown[i][0], unknown[i][1]
            if self.mf[r][c] != '?':
                del unknown[i]
            else:
                i += 1
        updates = self.do_handle_unknowns(unknown)
        #print('\n'.join([' '.join([str(x) for x in row]) for row in self.mf]))
        #print()
        if updates is None or self.bombs == 0:
            return
        return self.find_unknown_spaces(unknown)

    def make_return_object(self):
        """
        """
        obj = '\n'.join([' '.join([str(x) for x in row]) for row in self.mf])
        return '?' if '?' in obj else obj


def solve_mine(mine_field, n):
    """
    solves MineSweeper from input mine sweeper board
    """
    game = MineSweeper(mine_field, n)
    game.initial_board_scan()
    game.find_unknown_spaces(game.unknown)
    result = game.make_return_object()
    return result


if __name__ == "__main__":
    """
    MAIN APP, calls solve_mine
    """
    N = RESULT.count('x')
    RESULT = RESULT.split('\n')
    for x in range(len(RESULT)):
        RESULT[x] = RESULT[x].split(' ')
    answer = solve_mine(mine_field, N)
    print(answer)
