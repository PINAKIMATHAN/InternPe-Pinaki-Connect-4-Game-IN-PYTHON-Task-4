import tkinter as tk
from tkinter import messagebox
import time

class ConnectFour(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect Four")
        self.geometry("480x540")
        self.player_scores = {"Red": 0, "Yellow": 0}
        self.current_player = "Red"
        self.board_size = (6, 7)  # Default board size
        self.board = [['' for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.board_size[1] * 60, height=self.board_size[0] * 60, bg="#0077ff")
        self.canvas.grid(row=0, column=0, columnspan=7)

        self.scoreboard_frame = tk.Frame(self, bg="#0077ff")
        self.scoreboard_frame.grid(row=1, column=0, columnspan=7, pady=10)

        self.red_label = tk.Label(self.scoreboard_frame, text="Red: 0", font=('Helvetica', 14), bg="#0077ff", fg="white")
        self.red_label.grid(row=0, column=0, padx=10)

        self.yellow_label = tk.Label(self.scoreboard_frame, text="Yellow: 0", font=('Helvetica', 14), bg="#0077ff", fg="white")
        self.yellow_label.grid(row=0, column=1, padx=10)

        self.advanced_button = tk.Button(self, text="Advanced Mode", command=self.set_advanced_mode)
        self.advanced_button.grid(row=2, column=0, columnspan=7, pady=5)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.drop_piece)
        self.blinking_interval = 500  # milliseconds
        self.blinking = False

    def create_advanced_board_selection(self):
        self.board_size_selection_frame = tk.Frame(self, bg="#0077ff")
        self.board_size_selection_frame.grid(row=3, column=0, columnspan=7, pady=5)

        self.row_label = tk.Label(self.board_size_selection_frame, text="Rows:", font=('Helvetica', 12), bg="#0077ff", fg="white")
        self.row_label.grid(row=0, column=0, padx=5)

        self.row_entry = tk.Entry(self.board_size_selection_frame, width=5)
        self.row_entry.grid(row=0, column=1, padx=5)

        self.column_label = tk.Label(self.board_size_selection_frame, text="Columns:", font=('Helvetica', 12), bg="#0077ff", fg="white")
        self.column_label.grid(row=0, column=2, padx=5)

        self.column_entry = tk.Entry(self.board_size_selection_frame, width=5)
        self.column_entry.grid(row=0, column=3, padx=5)

        self.confirm_button = tk.Button(self.board_size_selection_frame, text="Confirm", command=self.confirm_board_size)
        self.confirm_button.grid(row=0, column=4, padx=5)

    def confirm_board_size(self):
        try:
            rows = int(self.row_entry.get())
            cols = int(self.column_entry.get())
            if rows < 4 or cols < 4:
                messagebox.showinfo("Invalid Size", "Rows and Columns must be at least 4.")
            else:
                self.board_size = (rows, cols)
                self.board_size_selection_frame.destroy()
                self.reset_board()
        except ValueError:
            messagebox.showinfo("Invalid Size", "Please enter valid integers for Rows and Columns.")

    def set_advanced_mode(self):
        self.create_advanced_board_selection()

    def draw_board(self):
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                x0 = col * 60 + 10
                y0 = row * 60 + 10
                x1 = x0 + 50
                y1 = y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#333333", fill="#eeeeee")

    def drop_piece(self, event):
        col = event.x // 60
        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = self.current_player
            self.draw_piece(row, col)
            if self.check_winner(row, col):
                messagebox.showinfo("Winner", f"{self.current_player} wins!")
                self.player_scores[self.current_player] += 1
                self.update_scoreboard()
                self.reset_board()
                return
            self.toggle_player()
            self.start_blinking()
        else:
            messagebox.showinfo("Invalid move", "This column is full.")

    def get_next_open_row(self, col):
        for row in range(self.board_size[0] - 1, -1, -1):
            if self.board[row][col] == '':
                return row
        return None

    def draw_piece(self, row, col):
        x = col * 60 + 35
        y = row * 60 + 35
        self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="#333333", fill=self.current_player)

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            count = 1
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < self.board_size[0] and 0 <= c < self.board_size[1] and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            r, c = row, col
            while True:
                r -= dr
                c -= dc
                if 0 <= r < self.board_size[0] and 0 <= c < self.board_size[1] and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                self.highlight_winner(row, col, dr, dc)
                return True
        return False

    def highlight_winner(self, row, col, dr, dc):
        r, c = row, col
        for _ in range(4):
            self.canvas.create_oval(c * 60 + 35 - 25, r * 60 + 35 - 25, c * 60 + 35 + 25, r * 60 + 35 + 25,
                                    outline="yellow", width=3)
            r += dr
            c += dc

    def toggle_player(self):
        self.current_player = "Yellow" if self.current_player == "Red" else "Red"

    def start_blinking(self):
        self.blinking = True
        self.blink_piece()

    def blink_piece(self):
        if self.blinking:
            self.canvas.delete("blinking")
            self.draw_piece(0, 0)  # Draw a piece at an unused location
            self.after(self.blinking_interval, self.toggle_blink)

    def toggle_blink(self):
        self.blinking = not self.blinking
        self.blink_piece()

    def update_scoreboard(self):
        self.red_label.config(text=f"Red: {self.player_scores['Red']}")
        self.yellow_label.config(text=f"Yellow: {self.player_scores['Yellow']}")

    def reset_board(self):
        self.board = [['' for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]
        self.canvas.delete("all")
        self.draw_board()
        self.current_player = "Red"

if __name__ == "__main__":
    app = ConnectFour()
    app.mainloop()
