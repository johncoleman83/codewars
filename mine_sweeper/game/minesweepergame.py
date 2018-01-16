#!/usr/bin/env python3
from datetime import datetime
import random
import sys

class MineSweeperGame():
    """
    Minesweeper Game
    """
    def __init__(self, height, width, mines):
        """
        initializes MineSweeper game solver
        """
        self.init_vals_and_verify_game_inputs(height, width, mines)
        self.B = {}
        self.revealed = set()
        self.initialize_board()

    def init_vals_and_verify_game_inputs(self, h, w, m):
        if 5 > h > 24 or 5 > w > 30 or m > h * w:
            raise Exception("invalid game coordinates")
        self.R = h
        self.C = w
        self.M = m

    def display_game(self):
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
                # print(piece, end=" ")
                print(piece if piece in self.revealed else '?', end=" ")
            piece = self.B.get((r, self.C - 1))
            print(piece if piece in self.revealed else '?')

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


def main_app():
    game = MineSweeperGame(10, 10, 10)
    game.display_game()

if __name__ == "__main__":
    """
    MAIN APP, calls solve_mine
    """
    main_app()
