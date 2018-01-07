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

class MineSweeper():
    """
    Minesweeper solver
    """
    def __init__(self, mine_field, bombs):
        """
        initializes MineSweeper game solver
        """
        if type(mine_field).__name__ == 'str':
            self.mf = mine_field.split('\n')
            for x in range(len(self.mf)):
                self.mf[x] = self.mf[x].split(' ')
        else:
            self.mf = mine_field
        self.bombs = bombs
        self.ROWS, self.COLS = len(self.mf), len(self.mf[0])
        self.borders = {}

    def generate_border_spaces(self, r, c, idx):
        """
        this containes all border spaces if on the board
        """
        self.borders[idx] = [True]
        b = [True]
        if r > 0:                                   b.append([r - 1, c])
        if r > 0 and c < self.COLS - 1:             b.append([r - 1, c + 1])
        if r > 0 and c > 0:                         b.append([r - 1, c - 1])
        if c < self.COLS - 1:                       b.append([r, c + 1])
        if c > 0:                                   b.append([r, c - 1])
        if r < self.ROWS - 1:                       b.append([r + 1, c])
        if r < self.ROWS - 1 and c < self.COLS - 1: b.append([r + 1, c + 1])
        if r < self.ROWS - 1 and c > 0:             b.append([r + 1, c - 1])
        self.borders[idx] = b

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
        if char == '?' and self.borders[idx][0] is False: return []
        for space in self.borders[idx][1:]:
            if char == 'int' == type(self.mf[space[0]][space[1]]).__name__:
                coords.append(space)
            elif self.mf[space[0]][space[1]] == char:
                coords.append(space)
        if char == '?' and len(coords) == 0 and test is False:
            self.borders[idx][0] = False
        return sorted(coords)

    def open_list(self, coords):
        """
        CALLS OPEN BASED ON INPUT LIST
        """
        for coord in coords:
            revealed = open(coord[0], coord[1])
            if type(revealed).__name__ == 'str':
                revealed = int(revealed)
            self.mf[coord[0]][coord[1]] = revealed

    def mark_bombs(self, coords):
        """
        Marks Bombs on input field from input coords
        """
        for coord in coords: self.mf[coord[0]][coord[1]] = 'x'

    def initial_board_scan_with_basic_logic(self):
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
                    c += 1
                    continue
                unknown = self.find_neighbors(idx, '?')
                if len(unknown) == 0:
                    c += 1
                    continue
                bombs = self.find_neighbors(idx, 'x')
                if type(square).__name__ == 'str' and square.isdigit():
                    square = int(square)
                    self.mf[r][c] = square
                if self.mf[r][c] == '0' or self.mf[r][c] == 0: self.open_list(unknown)
                elif len(bombs) == square: self.open_list(unknown)
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
        self.complete_border_neighbors()

    def scan_perimeter_pieces_for_bombs(self, perimeter):
        """
        scans for bombs in all perimeter integer pieces around unknown squares
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

    def find_integers_next_to_unknown_spaces(self, unknown):
        """
        finds all perimeter integer spaces around the unknown spaces
        """
        perimeter = set()
        for space in unknown:
            idx = space[0] * self.COLS + space[1]
            int_neighbors = self.find_neighbors(idx, 'int')
            for n in int_neighbors:
                idx = n[0] * self.COLS + n[1]
                perimeter.add(idx)
        perimeter = sorted(list(perimeter))
        for i in range(len(perimeter)):
            idx = perimeter[i]
            r = idx // self.COLS
            c = idx - (r * self.COLS)
            perimeter[i] = [r, c]
        return perimeter

    def guess_is_valid_bomb_placement(self, perimeter, unknown):
        """
        DETERMINES IF PERIMETER IS VALID BASED ON BOMB PLACEMENTS
        """
        for space in perimeter:
            r, c = space[0], space[1]
            square = self.mf[r][c]
            idx = r * self.COLS + c
            unknown = self.find_neighbors(idx, '?', test=True)
            bombs = self.find_neighbors(idx, 'x')
            if len(bombs) != square:
                return False
        return True

    def clean_field_of_bomb_guesses(self, unknown, i, end):
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

    def brute_force_combo_check(self, unknown, perimeter, bombs):
        """
        checks potential bomb combinations using a brute force algo
        """
        guesses = []
        for combo in itertools.combinations(
            [x for x in range(len(unknown))], bombs
        ):
            guess_combo = []
            for i in combo:
                r, c = unknown[i][0], unknown[i][1]
                self.mf[r][c] = 'x'
                guess_combo.append([r, c])
            if self.guess_is_valid_bomb_placement(perimeter, unknown) is True:
                numbers = self.clean_field_of_bomb_guesses(unknown, 0, len(unknown))
                guesses.append({
                    'bombs': guess_combo,
                    'numbers': numbers
                })
            else:
                self.clean_field_of_bomb_guesses(unknown, 0, len(unknown))
        return guesses

    def find_patterns_in_guesses(self, all_guesses):
        """
        Attempts to find all common bombs and numbers from all potential bomb patterns
        """
        com_n, com_b = {}, {}
        for guess in all_guesses:
            n, b = guess['numbers'], guess['bombs']
            nidx, bidx = [s[0] * self.COLS + s[1] for s in n], [s[0] * self.COLS + s[1] for s in b]
            if com_n == {}:
                com_n, com_b = set(nidx), set(bidx)
                continue
            com_n, com_b = com_n.intersection(set(nidx)), com_b.intersection(set(bidx))
        com_n = [[i // self.COLS, i - (i // self.COLS) * self.COLS] for i in com_n]
        com_b = [[i // self.COLS, i - (i // self.COLS) * self.COLS] for i in com_b]
        if len(com_n) > 0:
            self.open_list(list(com_n))
        if len(com_b) > 0:
            self.mark_bombs(list(com_b))
            self.bombs -= len(com_b)
        return 1 if len(com_n) > 0  or len(com_b) > 0 else 0

    def do_handle_unknown_spaces(self, unknown):
        """
        checks unrevealed spaces using a variety of logical computations
        """
        perimeter = self.find_integers_next_to_unknown_spaces(unknown)
        updates, all_guesses = 0, []
        potential_bombs = len(unknown) if len(unknown) < self.bombs else self.bombs
        total_unknown = self.find_unknown_spaces(total=True)
        start = self.bombs if len(total_unknown) == len(unknown) else 1
        for bombs in range(start, potential_bombs + 1):
            guesses = self.brute_force_combo_check(
                unknown, perimeter, bombs
            )
            for guess in guesses:
                all_guesses.append(guess)
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
        updates += self.scan_perimeter_pieces_for_bombs(perimeter)
        return None if updates == 0 else True

    def find_unknown_spaces(self, total=False):
        """
        returns a list of all unkown spaces that are not completely
        surrounded by '?' unknown spaces, except if input variable
        total is True, then all unknowns are returned
        """
        unknown = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.mf[r][c] == '?':
                    idx = r * self.COLS + c
                    int_neighbors = self.find_neighbors(idx, 'int')
                    bombs = self.find_neighbors(idx, 'x')
                    unknown_neighbors = self.find_neighbors(idx, '?')
                    known_spaces = len(int_neighbors) + len(bombs)
                    if (known_spaces > 0) or total is True:
                        unknown.append([r, c])
        return unknown

    def solve_remaining_unknowns(self):
        """
        recursively handles all remaining unknown sections until
        no changes are made or until the entire board is revealed
        """
        unknown = self.find_unknown_spaces()
        updates = self.do_handle_unknown_spaces(unknown)
        if updates is None or self.bombs == 0: return
        return self.solve_remaining_unknowns()

    def make_return_object(self):
        """
        returns string of current state of the mine field board
        """
        unknown = self.find_unknown_spaces(total=True)
        if self.bombs == 0:
            self.open_list(unknown)
            unknown = self.find_unknown_spaces(total=True)
        if self.bombs == len(unknown):
            self.mark_bombs(unknown)
        obj = '\n'.join([' '.join([str(x) for x in row]) for row in self.mf])
        return '?' if '?' in obj else obj


def solve_mine(mine_field, n):
    """
    solves MineSweeper from input mine sweeper board
    """
    game = MineSweeper(mine_field, n)
    game.initial_board_scan_with_basic_logic()
    game.solve_remaining_unknowns()
    result = game.make_return_object()
    return result

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
