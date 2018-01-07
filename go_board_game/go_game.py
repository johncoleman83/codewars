#!/usr/bin/env python3
"""
Go Board Game!
"""


class Go:
    """
    main class to handle go board game
    """

    ALPHAS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'
    ALL_SIDES = ["U", "R", "D", "L"]
    HANDICAP = {
        9 * 9: [
            [2, 6], [6, 2], [6, 6], [2, 6], [4, 4]
        ],
        13 * 13: [
            [3, 9], [9, 3], [9, 9], [3, 3], [6, 6],
            [6, 3], [6, 9], [3, 6], [9, 6]
        ],
        19 * 19: [
            [3, 15], [15, 3], [15, 15], [3, 3], [9, 9],
            [9, 3], [9, 15], [3, 9], [15, 9]
        ]
    }

    def __init__(self, height, width=None):
        """
        instantiates a new game based on input size of each dimension
        """
        self.__move = None
        self.size = [height, width]
        if height > 25 or (width is not None and width > 25):
            self.__error_handler(0)
        self.board = [height, width]
        self.turn = "black"
        self.__total_turns = 0
        self.__columns = dict([
            [a, ord(a) - (66 if ord(a) > ord("H") else 65)]
            for a in Go.ALPHAS[:self.width]
        ])
        self.__rows = dict([
            [row, self.height - row] for row in range(self.height, 0, -1)
        ])
        self.__stones = {"black": 'x', "white": 'o'}
        self.__initialize_game_state()

    @property
    def size(self):
        """
        prints and returns the size
        """
        return self.__size

    @size.setter
    def size(self, dimensions):
        """
        initializes the board with default settings
        """
        if dimensions[1] is None:
            self.height = self.width = dimensions[0]
        else:
            self.height, self.width = dimensions[0], dimensions[1]
        self.__size = {
            "height": self.height, "width": self.width
        }

    @property
    def board(self):
        """
        prints and returns the board
        """
        spaces = (2 if self.height < 10 else 3)
        alphas = ' '.join([a for a in Go.ALPHAS[:self.width]])
        top_edge = "{}{}".format(" " * spaces, alphas)
        print(top_edge)
        for row in range(self.height):
            numero = self.__rows[row + 1] + 1
            if self.height > 9:
                spaces = (1 if self.height - row > 9 else 2)
            else:
                spaces = 1
            print("{}{}".format(numero, " " * spaces), end="")
            for col in range(self.width - 1):
                print(self.__board[row][col], end=" ")
                if col == self.width - 2:
                    last = col + 1
            print(self.__board[row][last])
        return self.__board

    @board.setter
    def board(self, dimensions):
        """
        initializes the board with default settings
        """
        self.__board = [
            ['.' for row in range(self.width)] for col in range(self.height)
        ]

    def __error_handler(self, msg):
        """
        Handles all app error messages
        """
        ERROR = [
            "Board Size -> board size of {} x {} has a dimension larger than 25"
            .format(self.height, self.width),
            "Illegal Move -> play handicap stones after game play has begun",
            "Out of Bounds -> play {} is off the map or invalid"
            .format(self.__move),
            "Stone Conflict -> play {} already has a stone there"
            .format(self.__move),
            "Rollback -> rollback to before game started",
            "Self capture -> play {} is a self capture".format(self.__move),
            "Recreation -> play {} recreates a previous board position"
            .format(self.__move)
        ]
        raise ValueError("ERROR: {}".format(ERROR[msg]))

    def __initialize_game_state(self):
        """
        adds self.__this_state to the game states
        """
        self.__game_states = {
            ''.join([''.join(row) for row in self.__board]):
            [[self.__total_turns, self.turn]]
        }

    def handicap_stones(self, stones):
        """
        adds handicap stones to board at game start
        """
        if self.__total_turns > 0:
            self.__error_handler(1)
        size = self.height * self.width
        if size not in Go.HANDICAP:
            return
        this_places = Go.HANDICAP[size]
        for place in range(stones):
            row = this_places[place][0]
            col = this_places[place][1]
            self.__board[row][col] = 'x'

    def __opposite_color_stone(self, stone_color):
        """
        returns opposite color stone
        """
        return "white" if stone_color == "black" else "black"

    def reset(self):
        """
        resets game to beginning
        """
        self.turn = "black"
        self.__total_turns = 0
        del self.__game_states
        self.__board = [
            ['.' for row in range(self.width)] for col in range(self.height)
        ]
        self.__initialize_game_state()

    def pass_turn(self):
        """
        switches the queued color to move next
        """
        self.__total_turns += 1
        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"
        new_game_state = ''.join([''.join(row) for row in self.__board])
        if new_game_state in self.__game_states:
            self.__game_states[new_game_state].append(
                [self.__total_turns, self.turn])
        else:
            self.__game_states[new_game_state] = [
                [self.__total_turns, self.turn]]

    def __validate_coordinates(self, move, play=False):
        """
        verifies that coordinates are valid row coordinates
        """
        if len(move) == 3:
            row, col = move[0:2], move[2]
        else:
            row, col = move[0], move[1]
        if not row.isdigit():
            self.__error_handler(2)
        if not int(row) in self.__rows or not col in self.__columns:
            self.__error_handler(2)
        row, col = self.__rows[int(row)], self.__columns[col]
        if play == True and self.__board[row][col] != '.':
            self.__error_handler(3)
        return [row, col]

    def get_position(self, coordinates):
        """
        returns position stone of input coordinates
        """
        move = self.__validate_coordinates(coordinates, play=False)
        row, col = move[0], move[1]
        return self.__board[row][col]

    def __board_string_to_list(self, board_state):
        """
        converts board string to 2D array (list)
        """
        board_list = []
        index = 0
        for row in range(self.height):
            start = row * self.width
            end = start + self.width
            section = list(board_state[start:end])
            board_list.append(section)
        return board_list

    def __generate_next_steps(self, row, col):
        """
        generates a dictionary with next step meta data
        """
        next_step_data = {
            "U": [row == 0, row - 1, col, ["U", "R", "L"]],
            "R": [col == self.width - 1, row, col + 1, ["U", "R", "D"]],
            "D": [row == self.height - 1, row + 1, col, ["R", "D", "L"]],
            "L": [col == 0, row, col - 1, ["U", "D", "L"]]
        }
        return next_step_data


    def rollback(self, turns_back):
        """
        rollsback board state to previous state
        """
        turn = self.__total_turns - turns_back
        if turn < 0:
            self.__error_handler(4)
        new_game_states = {}
        for key, value in self.__game_states.items():
            for move in value:
                if move[0] <= turn:
                    new_game_states[key] = value
                if move[0] == turn:
                    state, meta = key, move
        self.__total_turns = meta[0]
        self.turn = meta[1]
        self.__board = self.__board_string_to_list(state)
        self.__game_states = new_game_states

    def __has_no_liberties(
            self, board_to_check, color, replace, position, previous):
        """
        checks board if self capture exists
        """
        row, col = position[0], position[1]
        liberty_stone = self.__stones[color]
        opposite_stone = self.__stones[self.__opposite_color_stone(color)]
        current_stone = board_to_check[row][col]
        if current_stone == opposite_stone or current_stone == '.':
            return False
        board_to_check[row][col] = replace
        next_step_data = self.__generate_next_steps(row, col)
        adjacents_blocked = 0
        if previous is None:
            next_recursive_calls = Go.ALL_SIDES
        else:
            next_recursive_calls = next_step_data[previous][3]
        for side in next_recursive_calls:
            if next_step_data[side][0] is True:
                adjacents_blocked += 1
                continue
            row_2, col_2 = next_step_data[side][1], next_step_data[side][2]
            edge_stone = board_to_check[row_2][col_2]
            if edge_stone == '.' and replace != '.':
                return 0
            if edge_stone == liberty_stone:
                adjacents_blocked += self.__has_no_liberties(
                    board_to_check, color, replace, [row_2, col_2], side
                )
            else:
                adjacents_blocked += 1
        if adjacents_blocked == 4 or (previous and adjacents_blocked == 3):
            return True
        else:
            return 0

    def __make_captures(self, next_step_data, board, capture_directive):
        """
        recursively makes a capture from known capturable sides
        """
        for side in capture_directive:
            row_2 = next_step_data[side][1]
            col_2 = next_step_data[side][2]
            liberty_color = self.__opposite_color_stone(self.turn)
            is_liberty = self.__has_no_liberties(
                board, liberty_color, '.', [row_2, col_2], None
            )

    def __find_capture_directive(self, next_step_data, row, col):
        """
        finds if there are any neighboring positions that have open liberties
        """
        capture_directive = []
        for side in Go.ALL_SIDES:
            board_copy = [copy_row.copy() for copy_row in self.__board]
            board_copy[row][col] = self.__stones[self.turn]
            if next_step_data[side][0] is True:
                continue
            row_2 = next_step_data[side][1]
            col_2 = next_step_data[side][2]
            liberty_color = self.__opposite_color_stone(self.turn)
            is_liberty = self.__has_no_liberties(
                board_copy, liberty_color, '*', [row_2, col_2], None
            )
            if is_liberty:
                capture_directive.append(side)
        return capture_directive

    def __do_handle_move(self, next_step_data, row, col):
        """
        handles move and capturing:
        """
        capture_directive = self.__find_capture_directive(
            next_step_data, row, col)
        board_copy = [copy_row.copy() for copy_row in self.__board]
        board_copy[row][col] = self.__stones[self.turn]
        self.__make_captures(next_step_data, board_copy, capture_directive)
        is_self_capturable = self.__has_no_liberties(
            board_copy, self.turn, '*', [row, col], None
        )
        if is_self_capturable is True:
            self.__error_handler(5)
        board_copy = [copy_row.copy() for copy_row in self.__board]
        board_copy[row][col] = self.__stones[self.turn]
        self.__make_captures(next_step_data, board_copy, capture_directive)
        potential_state = ''.join([''.join(row) for row in board_copy])
        previous_move = potential_state in self.__game_states
        if previous_move is True:
            self.__error_handler(6)
        self.__board[row][col] = self.__stones[self.turn]
        self.__make_captures(next_step_data, self.__board, capture_directive)
        self.pass_turn()

    def move(self, *args):
        """
        places piece on board
        """
        for move in args:
            self.__move = move
            move = self.__validate_coordinates(move, play=True)
            row, col = move[0], move[1]
            next_step_data = self.__generate_next_steps(row, col)
            self.__do_handle_move(next_step_data, row, col)

if __name__ == "__main__":
    """
    MAIN APP
    """
    print(
        "Usage:\n"
        "import go_game\n"
        "game = go_game.Go()"
    )
