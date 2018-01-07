#!/usr/bin/env python3
"""
Go Board Game!
"""
import go_game

ALPHAS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'

def app():
    """
    initializes game
    """
    print("What board dimensions would you like to play with?")
    while True:
        h = input("board number of rows (heigth: 1 - 25)  :  ")
        w = input("board number of columns (width 1 - 25) :  ")
        if h.isdigit() and w.isdigit():
            h, w = int(h), int(w)
            try:
                game = go_game.Go(h, w)
                break
            except Exception as e:
                print(e)
        else:
            print("Invalid dimensions, please select again")
    while True:
        game.board
        print("It is {}'s turn. What position would you like to play?"
              .format(game.turn))
        row = input("    row ({} - {})  :  ".format(game.height, 1))
        col = input("    col ({} - {}) :  ".format("A", ALPHAS[game.width - 1]))
        try:
            game.move("{}{}".format(row, col))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    """
    MAIN APP
    """
    app()
