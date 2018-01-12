#!/usr/bin/env python3

class SudokuSolver():

    def __init__(self, puzzle):
        self.p_input = puzzle
        self.generate_variables()
        while self.unsolved > 0:
            self.brute_force_solver()

    def generate_variables(self):
        self.all_ints = set(x for x in range(0, 10))
        self.puzzle, self.exclusion = {}, {}
        self.exclusion = {}
        self.g, self.c, self.r = [
            [[] for x in range(9)], [[] for x in range(9)], [[] for x in range(9)]
        ]
        self.unsolved = 0
        for r in range(9):
            for c in range(9):
                val = int(self.p_input[r][c])
                if val == 0: self.unsolved += 1
                self.puzzle[(r, c)] = val
                self.exclusion[(r, c)] = set([0])
                self.c[c].append((r, c))
                self.r[r].append((r, c))
                self.g[r // 3 * 3 + c // 3].append((r, c))

    def display(self):
        game = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.puzzle[(r, c)])
            game.append(row)
        return game

    def brute_force_solver(self):
        for r in range(9):
            for c in range(9):
                val = self.puzzle[(r, c)]
                if val > 0:
                    self.exclusion[(r, c)] = set(x for x in range(0, 10) if x != val)
                    continue
                for coord in self.r[r]: self.exclusion[(r, c)].add(self.puzzle.get(coord))
                for coord in self.c[c]: self.exclusion[(r, c)].add(self.puzzle.get(coord))
                for coord in self.g[r // 3 * 3 + c // 3]: self.exclusion[(r, c)].add(self.puzzle.get(coord))
                if len(self.exclusion[(r, c)]) == 9:
                    self.unsolved -= 1
                    val_set = self.all_ints - self.exclusion[(r, c)]
                    self.puzzle[(r, c)] = val_set.pop()

puzzle = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]
game = SudokuSolver(puzzle)
answer = game.display()
for r in answer:
    print(r)
