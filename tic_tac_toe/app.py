#!/usr/bin/env python3
"""
tic tac toe v. 0.0.1
"""
class TicTacToeGame(object):
    """
    Tic Tac Toe Game Class with Board and game functions
    """
    def __init__(self):
        self.positions = """
   {} | {} | {}
   ---------
   {} | {} | {}
   ---------
   {} | {} | {}
""".format(
    1, 2, 3, 4, 5, 6, 7, 8, 9
)
        self.board = [
            ["\033[90m1\033[30m", "\033[90m2\033[30m", "\033[90m3\033[30m"],
            ["\033[90m4\033[30m", "\033[90m5\033[30m", "\033[90m6\033[30m"],
            ["\033[90m7\033[30m", "\033[90m8\033[30m", "\033[90m9\033[30m"]
        ]
        self.next_player = "X"

    @property
    def winner(self):
        """
        retreives winner if there is one
        """
        rotated = []
        rotated[:] = zip(*self.board[::-1])
        for row in self.board:
            if row.count('\x1b[32mX\x1b[30m') == 3 or row.count("\x1b[32mO\x1b[30m") == 3:
                return row[0]
        for row in rotated:
            if row.count('\x1b[32mX\x1b[30m') == 3 or row.count('\x1b[32mO\x1b[30m') == 3:
                return row[0]
        if (self.board[0][0] == self.board[1][1] and
            self.board[0][0] == self.board[2][2] and
            self.board[0][0] != " "):
            return self.board[0][0]
        if (self.board[0][2] == self.board[1][1] and
            self.board[0][2] == self.board[2][0] and
            self.board[0][2] != " "):
            return self.board[0][0]
        plays = 0
        for row in self.board:
            for col in row:
               if "X" in col or "O" in col:
                    plays += 1
               else:
                    break
        if plays == 9:
            return "No Winner"
        return None

    @winner.setter
    def winner(self):
        """
        sets winner to None, never used
        """
        self.__winner = None

    def __repr__(self):
        """
        string representation of game
        prints board with all moves
        or prints position of unplayed tiles
        """
        b = self.board
        display = """
   {} | {} | {}
   ---------
   {} | {} | {}
   ---------
   {} | {} | {}
""".format(
    b[0][0], b[0][1], b[0][2],
    b[1][0], b[1][1], b[1][2],
    b[2][0], b[2][1], b[2][2]
)
        return display

    def make_move(self, position):
        """
        function handles making a move
        """
        b = self.board
        options = {
            1: b[0][0],
            2: b[0][1],
            3: b[0][2],
            4: b[1][0],
            5: b[1][1],
            6: b[1][2],
            7: b[2][0],
            8: b[2][1],
            9: b[2][2]
        }
        if "X" in options[position] or "O" in options[position]:
            return False
        i = 1
        row = 0
        for row in range(3):
            col = 0
            for col in range(3):
                if i == position:
                    self.board[row][col] = (
                        "{}{}{}".format("\033[32m", self.next_player, "\033[30m"))
                    return True
                i += 1
        return False

    def switch_player(self):
        """
        Switches next player that is queued to move
        """
        if self.next_player == "X":
            self.next_player = "O"
        else:
            self.next_player = "X"

def start_play():
    """
    initiates playing a game of tic tac toe
    creates game object
    """
    play = input("Would you like to play? Type 'Y' or 'y' to play: ")
    if "y" in play.lower():
        game = TicTacToeGame()
    else:
        print("Your selection was one of not selecting to play.  Goodbye!")
        exit(0)
    next_player = None
    while next_player is None:
        next_player = input("Who should be the first player? 'X' or 'O': ")
        if 'x' in next_player.lower():
            game.next_player = "X"
        elif 'o' in next_player.lower():
            game.next_player = "O"
        else:
            next_player = None
    game_loop(game)

def game_loop(game):
    """
    loops through moves modifying the game object
    """
    while game.winner is None:
        print("It is now [ {} ] player's turn".format(game.next_player))
        print("What position would you like to play?")
        print("type 'exit' to quit")
        print(game)
        position = input("your selection: ")
        if position.lower() == 'exit':
            break
        if not position.isdigit() or int(position) > 9 or int(position) < 1:
            print("\nPlease input a valid position\n")
            continue
        else:
            if not game.make_move(int(position)):
                print("\nPlease input a valid position\n")
                continue
            else:
                print("\nNice move\n")
                game.switch_player()
    # end game
    print("\nAnd the winner is: {}\n\n".format(game.winner))
    print(game)


if __name__ == "__main__":
    """
    MAIN APP
    """
    start_play()
