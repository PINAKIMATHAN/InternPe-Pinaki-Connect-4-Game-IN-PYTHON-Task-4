import tkinter as tk
from tkinter import messagebox

class ConnectFour(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect Four")
        self.geometry("480x540")
        self.current_player = "red"
        self.board = [['' for _ in range(7)] for _ in range(6)]
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=420, height=420, bg="#0077ff")
        self.canvas.grid(row=0, column=0, columnspan=7)

        self.scoreboard = tk.Label(self, text="Red: 0   Yellow: 0", font=('Helvetica', 14), bg="#0077ff", fg="white")
        self.scoreboard.grid(row=1, column=0, columnspan=7, pady=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.drop_piece)

    def draw_board(self):
        for row in range(6):
            for col in range(7):
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
                messagebox.showinfo("Winner", f"{self.current_player.capitalize()} wins!")
                self.reset_board()
                return
            self.toggle_player()
        else:
            messagebox.showinfo("Invalid move", "This column is full.")

    def get_next_open_row(self, col):
        for row in range(5, -1, -1):
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
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            r, c = row, col
            while True:
                r -= dr
                c -= dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
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
        self.current_player = "yellow" if self.current_player == "red" else "red"

    def reset_board(self):
        self.board = [['' for _ in range(7)] for _ in range(6)]
        self.canvas.delete("all")
        self.draw_board()
        self.current_player = "red"

if __name__ == "__main__":
    app = ConnectFour()
    app.mainloop()
