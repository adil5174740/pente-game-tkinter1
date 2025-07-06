import tkinter as tk
from tkinter import messagebox
from pente import PenteGame
import json

class PenteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pente Game")
        self.root.geometry("600x600")
        self.game = PenteGame()
        self.frames = {}
        self.create_frames()
        self.show_frame("menu")

    def create_frames(self):
        # Menu Screen
        menu_frame = tk.Frame(self.root)
        tk.Label(menu_frame, text="Welcome to Pente", font=("Helvetica", 20)).pack(pady=20)
        tk.Button(menu_frame, text="Start Game", command=lambda: self.show_frame("game")).pack(pady=10)
        tk.Button(menu_frame, text="Rules", command=lambda: self.show_frame("rules")).pack(pady=10)
        tk.Button(menu_frame, text="Exit", command=self.root.quit).pack(pady=10)
        self.frames["menu"] = menu_frame

        # Game Screen
        game_frame = tk.Frame(self.root)
        self.board_buttons = [[None for _ in range(13)] for _ in range(13)]
        for i in range(13):
            for j in range(13):
                btn = tk.Button(game_frame, text="", width=2, height=1,
                                command=lambda x=i, y=j: self.on_click(x, y))
                btn.grid(row=i, column=j)
                self.board_buttons[i][j] = btn
        self.turn_label = tk.Label(game_frame, text="Turn: Blue")
        self.turn_label.grid(row=14, column=0, columnspan=13)
        self.capture_label = tk.Label(game_frame, text="Captures - Blue: 0, Yellow: 0")
        self.capture_label.grid(row=15, column=0, columnspan=13)
        tk.Button(game_frame, text="Back to Menu", command=lambda: self.show_frame("menu")).grid(row=16, column=0, columnspan=13)
        self.frames["game"] = game_frame

        # Rules Screen
        rules_frame = tk.Frame(self.root)
        rules_text = (
            "Pente Rules:\n"
            "- Two players alternate turns placing stones.\n"
            "- First to get 5 in a row (horizontal, vertical, diagonal) wins.\n"
            "- Capturing two opponent stones also scores.\n"
            "- Capture 10 stones (5 pairs) to win."
        )
        tk.Label(rules_frame, text=rules_text, justify="left").pack(pady=20)
        tk.Button(rules_frame, text="Back to Menu", command=lambda: self.show_frame("menu")).pack()
        self.frames["rules"] = rules_frame

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def on_click(self, x, y):
        if self.game.board[x][y] != ".":
            return
        if not self.game.place_stone(x, y):
            return

        self.update_board()
        if self.game.check_five_in_a_row(x, y):
            self.save_result(f"{self.game.turn} wins by 5 in a row")
            messagebox.showinfo("Game Over", f"{self.game.turn} wins by 5 in a row!")
            self.reset_game()
        elif self.game.check_capture_win():
            self.save_result(f"{self.game.turn} wins by capturing 5 pairs")
            messagebox.showinfo("Game Over", f"{self.game.turn} wins by capturing 5 pairs!")
            self.reset_game()
        else:
            self.game.switch_turn()
        self.update_board()

    def update_board(self):
        for i in range(13):
            for j in range(13):
                text = self.game.board[i][j]
                if text == "B":
                    self.board_buttons[i][j]["bg"] = "blue"
                elif text == "Y":
                    self.board_buttons[i][j]["bg"] = "yellow"
                else:
                    self.board_buttons[i][j]["bg"] = "SystemButtonFace"
        self.turn_label.config(text=f"Turn: {'Blue' if self.game.turn == 'B' else 'Yellow'}")
        self.capture_label.config(
            text=f"Captures - Blue: {self.game.captures['B']}, Yellow: {self.game.captures['Y']}")

    def reset_game(self):
        self.game = PenteGame()
        self.update_board()

    def save_result(self, result):
        try:
            with open("match_history.json", "r") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        history.append({"result": result})

        with open("match_history.json", "w") as file:
            json.dump(history, file, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = PenteGUI(root)
    root.mainloop()
