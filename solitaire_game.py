class SolitaireGame:
    def __init__(self, board_type="English", board_size=7):
        self.board_type = board_type
        self.board_size = board_size
        self.board = []
        self.new_game()

    def new_game(self):
        if self.board_type == "English":
            self.create_english_board()

        elif self.board_type == "Hexagon":
            self.create_hexagon_board()

        elif self.board_type == "Diamond":
            self.create_diamond_board()

    # --------------------------------
    # ENGLISH BOARD
    # --------------------------------

    def create_english_board(self):
        size = self.board_size

        # Make sure the size is odd so there is one center position
        if size % 2 == 0:
            size += 1
            self.board_size = size

        # Minimum size
        if size < 5:
            size = 5
            self.board_size = size

        self.board = []

        center = size // 2

        # Width of the center section
        arm_width = 3

        arm_start = center - 1
        arm_end = center + 1

        for row in range(size):
            current_row = []

            for col in range(size):

                # Middle horizontal section
                if arm_start <= row <= arm_end:
                    current_row.append(1)

                # Top and bottom vertical sections
                elif arm_start <= col <= arm_end:
                    current_row.append(1)

                # Position is not part of the board
                else:
                    current_row.append(-1)

            self.board.append(current_row)

        # Empty center position
        self.board[center][center] = 0

    # --------------------------------
    # HEXAGON BOARD
    # --------------------------------

    def create_hexagon_board(self):
        # Keep our current Hexagon for now

        self.board = [
            [-1, -1, 1, 1, 1, 1, -1, -1],
            [-1, 1, 1, 1, 1, 1, 1, -1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [-1, 1, 1, 1, 1, 1, 1, -1],
            [-1, -1, 1, 1, 1, 1, -1, -1]
        ]

        self.board_size = 7

    # --------------------------------
    # DIAMOND BOARD
    # --------------------------------

    def create_diamond_board(self):
        self.board = [
            [-1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, 1, 1, 1, 1, 1, -1],
            [1, 1, 1, 0, 1, 1, 1],
            [-1, 1, 1, 1, 1, 1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1]
        ]

        self.board_size = 7

    # --------------------------------
    # GETTERS
    # --------------------------------

    def get_board(self):
        return self.board

    def get_board_type(self):
        return self.board_type

    def get_board_size(self):
        return self.board_size

    # --------------------------------
    # CHECK BOARD POSITION
    # --------------------------------

    def is_inside_board(self, row, col):
        if row < 0 or row >= len(self.board):
            return False

        if col < 0 or col >= len(self.board[row]):
            return False

        if self.board[row][col] == -1:
            return False

        return True

    # --------------------------------
    # MAKE MOVE
    # --------------------------------

    def make_move(
        self,
        start_row,
        start_col,
        end_row,
        end_col
    ):
        if not self.is_inside_board(start_row, start_col):
            return False

        if not self.is_inside_board(end_row, end_col):
            return False

        # Starting position must contain a peg
        if self.board[start_row][start_col] != 1:
            return False

        # Ending position must be empty
        if self.board[end_row][end_col] != 0:
            return False

        row_difference = abs(
            end_row - start_row
        )

        col_difference = abs(
            end_col - start_col
        )

        # Horizontal, vertical, or diagonal jump
        valid_move = (
            (
                row_difference == 2
                and col_difference == 0
            )
            or
            (
                row_difference == 0
                and col_difference == 2
            )
            or
            (
                row_difference == 2
                and col_difference == 2
            )
        )

        if not valid_move:
            return False

        middle_row = (
            start_row + end_row
        ) // 2

        middle_col = (
            start_col + end_col
        ) // 2

        if not self.is_inside_board(
            middle_row,
            middle_col
        ):
            return False

        # Must jump over another peg
        if self.board[middle_row][middle_col] != 1:
            return False

        # Perform move
        self.board[start_row][start_col] = 0
        self.board[middle_row][middle_col] = 0
        self.board[end_row][end_col] = 1

        return True

    # --------------------------------
    # CHECK FOR VALID MOVES
    # --------------------------------

    def has_valid_moves(self):
        directions = [
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
            (-2, -2),
            (-2, 2),
            (2, -2),
            (2, 2)
        ]

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                if self.board[row][col] == 1:

                    for row_change, col_change in directions:

                        end_row = row + row_change
                        end_col = col + col_change

                        if self.is_inside_board(
                            end_row,
                            end_col
                        ):
                            middle_row = (
                                row + end_row
                            ) // 2

                            middle_col = (
                                col + end_col
                            ) // 2

                            if (
                                self.is_inside_board(
                                    middle_row,
                                    middle_col
                                )
                                and
                                self.board[
                                    middle_row
                                ][middle_col] == 1
                                and
                                self.board[
                                    end_row
                                ][end_col] == 0
                            ):
                                return True

        return False

    # --------------------------------
    # GAME OVER
    # --------------------------------

    def is_game_over(self):
        return not self.has_valid_moves()

    # --------------------------------
    # COUNT PEGS
    # --------------------------------

    def count_pegs(self):
        count = 0

        for row in self.board:
            for position in row:

                if position == 1:
                    count += 1

        return count