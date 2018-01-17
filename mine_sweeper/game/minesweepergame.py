#!/usr/bin/env python3
from datetime import datetime
import random
import re
import sys

class MineSweeperGame():
    """
    Minesweeper Game
    """
    def __init__(self, *args):
        """
        initializes MineSweeper game solver
        """
        self.init_vals_and_verify_game_inputs(args[0])

    def tokenize(self, s):
        if s == "":
            return []
        regex = re.compile("([0-9]*)")
        tokens = regex.findall(s)
        return [s for s in tokens if not s.isspace() and s != '']

    def tokenize_input(self, choice):
        tokens = self.tokenize(choice)
        if len(tokens) == 2:
            return int(tokens[0]), int(tokens[1])
        else:
            return None, None

    def tokenize_args(self, s):
        tokens = self.tokenize(s)
        if len(tokens) == 3:
            return int(tokens[0]), int(tokens[1]), int(tokens[2])
        else:
            return None, None, None

    def init_vals_and_verify_game_inputs(self, args):
        w, h, m = self.tokenize_args(args)
        if w is None or h is None or m is None or 5 > h > 24 or 5 > w > 30 or m > h * w:
            raise Exception("invalid game coordinates")
        self.R = h
        self.C = w
        self.M = m
        self.B = {}
        self.revealed = set()
        self.initialize_board()
        self.finished = False
        if self.more_unrevealed_spaces() is False:
            raise Exception("this board is invalid due to already having been completed")

    def display_game(self, reveal=False):
        print("   ", end="")
        for x in range(self.C - 1):
            print(x, end=" ")
        print(self.C - 1)
        print("  -", end="")
        for _ in range(self.C - 1):
            print("--", end="")
        print("-")
        for r in range(self.R):
            print(r, end="| ")
            for c in range(self.C - 1):
                piece = self.B.get((r, c))
                if reveal is True:
                    print(piece, end=" ")
                else:
                    print(piece if (r, c) in self.revealed else '?', end=" ")
            piece = self.B.get((r, self.C - 1))
            if reveal is True:
                print(piece)
            else:
                print(piece if (r, self.C - 1) in self.revealed else '?')

    def set_space_values(self):
        for r in range(self.R):
            for c in range(self.C):
                if self.B[(r, c)] == '*': continue
                neighbors = [
                    (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                    (r, c - 1), (r, c + 1),
                    (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)
                ]
                mines = 0
                for n in neighbors:
                    mines += 1 if self.B.get(n, 0) == '*' else 0
                self.B[(r, c)] = mines

    def place_mines(self):
        mines = self.M
        game_coords = list(self.B.keys())
        coord_range = len(game_coords) - 1
        while mines > 0:
            mine_index = random.randint(0, coord_range)
            mine_coord = game_coords[mine_index]
            if self.B.get(mine_coord) != '*':
                self.B[mine_coord] = '*'
                mines -= 1

    def initialize_board(self):
        for r in range(self.R):
            for c in range(self.C):
                self.B[(r, c)] = 0
        self.place_mines()
        self.set_space_values()

    def more_unrevealed_spaces(self):
        if len(self.revealed) + self.M < self.R * self.C:
            return True
        return False

    def game_loop(self):
        while self.finished == False:
            self.display_game()
            print("Your move must be an input of 2 space separated integers"
                  " e.g. row column: '5 5'")
            choice = input("what position would you like to reveal?  ")
            if choice == "quit":
                break
            r, c = self.tokenize_input(choice)
            if r is None or c is None:
                print("invalid input, please try again")
                continue
            space = self.B.get((r, c), None)
            if space is None:
                print("invalid board space, please try again")
            elif space == '*':
                print()
                print("BOOOOM!!")
                print()
                self.display_game(reveal=True)
                self.finished = True
            elif (r, c) in self.revealed:
                print("space is already revealed, please try again")
            else:
                self.revealed.add((r, c))
                if self.more_unrevealed_spaces() is False:
                    self.finished = True
                    print("congratulations!!")
                    self.display_game(reveal=True)

def main_app():
    print("What board dimensions would you like?")
    print("input 3 space separated values: board width, height, and mine count")
    choice = input("e.g. 10 10 10   ")
    game = MineSweeperGame(choice)
    game.game_loop()

if __name__ == "__main__":
    """
    MAIN APP, calls solve_mine
    """
    main_app()
