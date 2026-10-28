import tkinter as tk
from tkinter import messagebox
from solitaire_game import SolitaireGame


class SolitaireGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.geometry("900x950")

        self.game = SolitaireGame("English", 7)
        self.selected_position = None

        # -----------------------------
        # TITLE
        # -----------------------------
        title_label = tk.Label(
            self.root,
            text="Peg Solitaire Game",
            font=("Arial", 26, "bold")
        )
        title_label.pack(pady=(15, 10))

        # -----------------------------
        # CONTROLS
        # -----------------------------
        controls_frame = tk.Frame(self.root)
        controls_frame.pack()

        tk.Label(
            controls_frame,
            text="Select Board Type:",
            font=("Arial", 11, "bold")
        ).pack(pady=(0, 3))

        self.board_type_var = tk.StringVar(value="English")

        tk.Radiobutton(
            controls_frame,
            text="English",
            variable=self.board_type_var,
            value="English",
            font=("Arial", 11)
        ).pack()

        tk.Radiobutton(
            controls_frame,
            text="Hexagon",
            variable=self.board_type_var,
            value="Hexagon",
            font=("Arial", 11)
        ).pack()

        tk.Radiobutton(
            controls_frame,
            text="Diamond",
            variable=self.board_type_var,
            value="Diamond",
            font=("Arial", 11)
        ).pack()

        # -----------------------------
        # BOARD SIZE
        # -----------------------------
        tk.Label(
            controls_frame,
            text="Board Size:",
            font=("Arial", 11, "bold")
        ).pack(pady=(8, 3))

        self.board_size_var = tk.IntVar(value=7)

        self.board_size_spinbox = tk.Spinbox(
            controls_frame,
            from_=5,
            to=9,
            textvariable=self.board_size_var,
            width=5,
            font=("Arial", 11)
        )
        self.board_size_spinbox.pack()

        # -----------------------------
        # NEW GAME
        # -----------------------------
        tk.Button(
            controls_frame,
            text="New Game",
            command=self.start_new_game,
            font=("Arial", 11)
        ).pack(pady=10)

        # -----------------------------
        # STATUS
        # -----------------------------
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11)
        )
        self.status_label.pack(pady=(5, 5))

        # -----------------------------
        # BOARD AREA
        # -----------------------------
        self.board_frame = tk.Frame(self.root)

        self.board_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.display_board()
        self.update_status()

    # =====================================================
    # NEW GAME
    # =====================================================

    def start_new_game(self):

        board_type = self.board_type_var.get()
        board_size = self.board_size_var.get()

        self.game = SolitaireGame(
            board_type,
            board_size
        )

        self.selected_position = None

        # Update displayed size if game adjusted it
        self.board_size_var.set(
            self.game.get_board_size()
        )

        self.display_board()
        self.update_status()

    # =====================================================
    # DISPLAY BOARD
    # =====================================================

    def display_board(self):

        # Remove the old board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        board = self.game.get_board()

        if self.game.get_board_type() == "Hexagon":
            self.display_hexagon(board)
        else:
            self.display_grid_board(board)

    # =====================================================
    # ENGLISH / DIAMOND BOARD
    # =====================================================

    def display_grid_board(self, board):

        board_holder = tk.Frame(
            self.board_frame
        )

        board_holder.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Make size 9 slightly smaller
        if len(board) >= 9:
            font_size = 10
        else:
            font_size = 13

        for row in range(len(board)):

            for col in range(len(board[row])):

                value = board[row][col]

                # Skip positions outside the board
                if value == -1:
                    continue

                if value == 1:
                    symbol = "●"
                else:
                    symbol = "○"

                button = tk.Button(
                    board_holder,
                    text=symbol,
                    font=("Arial", font_size),
                    width=2,
                    height=1,
                    command=lambda r=row, c=col:
                    self.position_clicked(r, c)
                )

                button.grid(
                    row=row,
                    column=col,
                    padx=1,
                    pady=1
                )

    # =====================================================
    # HEXAGON BOARD
    # =====================================================

    def display_hexagon(self, board):

        board_holder = tk.Frame(
            self.board_frame
        )

        board_holder.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Each row gets its own frame so it stays centered
        for row_index, row in enumerate(board):

            row_frame = tk.Frame(
                board_holder
            )

            row_frame.pack(
                pady=1
            )

            for col_index, value in enumerate(row):

                # Skip positions outside the board
                if value == -1:
                    continue

                if value == 1:
                    symbol = "●"
                else:
                    symbol = "○"

                button = tk.Button(
                    row_frame,
                    text=symbol,
                    font=("Arial", 11),
                    width=2,
                    height=1,
                    command=lambda r=row_index, c=col_index:
                    self.position_clicked(r, c)
                )

                button.pack(
                    side="left",
                    padx=1
                )

    # =====================================================
    # STATUS
    # =====================================================

    def update_status(self):

        board_type = self.game.get_board_type()
        pegs = self.game.count_pegs()

        self.status_label.config(
            text=(
                f"Board: {board_type} | "
                f"Pegs Remaining: {pegs}"
            )
        )

    # =====================================================
    # PLAYER CLICKS BOARD
    # =====================================================

    def position_clicked(self, row, col):

        board = self.game.get_board()

        # -----------------------------
        # FIRST CLICK
        # -----------------------------
        if self.selected_position is None:

            # Player must select a peg
            if board[row][col] == 1:

                self.selected_position = (
                    row,
                    col
                )

                self.status_label.config(
                    text=(
                        f"Selected peg at "
                        f"({row}, {col})"
                    )
                )

            else:

                self.status_label.config(
                    text="Please select a peg."
                )

            return

        # -----------------------------
        # SECOND CLICK
        # -----------------------------
        start_row, start_col = (
            self.selected_position
        )

        move_successful = self.game.make_move(
            start_row,
            start_col,
            row,
            col
        )

        self.selected_position = None

        # -----------------------------
        # VALID MOVE
        # -----------------------------
        if move_successful:

            self.display_board()
            self.update_status()

            remaining_pegs = (
                self.game.count_pegs()
            )

            # ---------------------------------
            # WIN: ONLY ONE PEG REMAINS
            # ---------------------------------
            if remaining_pegs == 1:

                messagebox.showinfo(
                    "Game Over",
                    (
                        "You won!\n\n"
                        "Only 1 peg remains."
                    )
                )

            # ---------------------------------
            # GAME OVER: NO MOVES REMAIN
            # ---------------------------------
            elif self.game.is_game_over():

                messagebox.showinfo(
                    "Game Over",
                    (
                        "No valid moves remain.\n\n"
                        f"Pegs remaining: "
                        f"{remaining_pegs}"
                    )
                )

        # -----------------------------
        # INVALID MOVE
        # -----------------------------
        else:

            self.status_label.config(
                text="Invalid move. Try again."
            )


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SolitaireGUI(root)

    root.mainloop()