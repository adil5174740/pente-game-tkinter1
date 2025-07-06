import tkinter as tk

def launch_home_screen():
    home = tk.Tk()
    home.title("Welcome to Pente")

    label = tk.Label(home, text="🎮 Pente Game", font=("Arial", 24))
    label.pack(pady=20)

    start_btn = tk.Button(home, text="Start Game", command=home.destroy)
    start_btn.pack(pady=10)

    instructions = tk.Label(home, text="Get 5 in a row to win!", font=("Arial", 12))

