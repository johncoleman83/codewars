#!/usr/bin/env python3
import random

class TTTBoard():
    def __init__(self):
        self.queued_player = 'X'
        self.init_board()
        self.plays = 0

    def init_board(self):
        self.board = []
        count = 1
        for _ in range(3):
            row = []
            for __ in range(3):
                row.append(count)
                count += 1
            self.board.append(row)

    def display_board(self):
        b = self.board
        game_display = """
 {} | {} | {}
 ----------
 {} | {} | {}
 ----------
 {} | {} | {}
""".format(b[0][0], b[0][1], b[0][2], b[1][0], b[1][1], b[1][2], b[2][0], b[2][1], b[2][2])
        print(game_display)

    def switch_queued_player(self):
        if self.queued_player == 'X':
            self.queued_player = 'O'
        else:
            self.queued_player = 'X'

    def play_position(self, position):
        if not position.isdigit():
            return False
        position = int(position)
        if not 1 <= position <= 9:
            return False
        index = 1
        for row in range(3):
            for col in range(3):
                if index == position:
                    if type(self.board[row][col]) != int:
                        return False
                    self.board[row][col] = self.queued_player
                    self.plays += 1
                    return True
                index += 1
        return False

    def check_winner(self):
        b = self.board
        for i in range(3):
            if len(set(b[i])) == 1 and type(b[i][0]) != int:
                return b[i][0]
            if (len(set([b[0][i], b[1][i], b[2][i]])) == 1
                and type(b[0][i]) != int):
                return b[0][i]
        if len(set([b[0][0], b[1][1], b[2][2]])) == 1 and type(b[1][1]) != int:
            return b[1][1]
        if len(set([b[0][2], b[1][1], b[2][0]])) == 1 and type(b[1][1]) != int:
            return b[1][1]
        return None

    def computer_play(self):
        count = sum([1 if type(c) == int else 0 for r in self.board for c in r])
        move = random.randint(1, count)
        for row in range(3):
            for col in range(3):
                if type(self.board[row][col]) == int:
                    move -= 1
                    if move == 0:
                        self.board[row][col] = self.queued_player
                        self.plays += 1
                        return True
        return False

    def game_loop(self):
        while True:
            self.display_board()
            print('pick the number of the position you would like to play')
            position = None
            while position is None:
                position = input('an integer 1 - 9 only ')
                if self.play_position(position) is False:
                    position = None
                    print('invalid game choice, please play again')
            if self.check_winner() is not None:  break
            if self.plays == 9:                  break
            self.switch_queued_player()
            while self.computer_play() is False: pass
            if self.check_winner() is not None:  break
            self.switch_queued_player()
        print('and the winner is...')
        print(self.check_winner())

def main_app():
    game = TTTBoard()
    game.game_loop()


if __name__ == "__main__":
    main_app()
