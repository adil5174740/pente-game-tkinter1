# pente_game.py

SIZE = 13
EMPTY = "."
BLUE = "B"
YELLOW = "Y"

class PenteGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        self.turn = BLUE  # Blue starts the game
        self.captures = {BLUE: 0, YELLOW: 0}

    def print_board(self):
        print("   " + " ".join(f"{i:2}" for i in range(SIZE)))
        for idx, row in enumerate(self.board):
            print(f"{idx:2} " + "  ".join(row))
        print(f"\nCaptures -> Blue: {self.captures[BLUE]}, Yellow: {self.captures[YELLOW]}")

    def switch_turn(self):
        self.turn = YELLOW if self.turn == BLUE else BLUE

    def in_bounds(self, x, y):
        return 0 <= x < SIZE and 0 <= y < SIZE

    def place_stone(self, x, y):
        if not self.in_bounds(x, y):
            print("Move out of bounds! Please choose a row and column between 0 and 12.")
            return False
        if self.board[x][y] != EMPTY:
            print("Cell already occupied! Please choose an empty cell.")
            return False
        self.board[x][y] = self.turn
        self.check_captures(x, y)
        return True

    def check_captures(self, x, y):
        enemy = YELLOW if self.turn == BLUE else BLUE
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            for direction in [1, -1]:  # Check both directions
                px = x + direction * dx
                py = y + direction * dy
                qx = x + 2 * direction * dx
                qy = y + 2 * direction * dy
                rx = x + 3 * direction * dx
                ry = y + 3 * direction * dy

                if all(self.in_bounds(a, b) for a, b in [(px, py), (qx, qy), (rx, ry)]):
                    if (self.board[px][py] == enemy and
                        self.board[qx][qy] == enemy and
                        self.board[rx][ry] == self.turn):
                        # Capture
                        self.board[px][py] = EMPTY
                        self.board[qx][qy] = EMPTY
                        self.captures[self.turn] += 2
                        print(f"{self.turn} captured stones at ({px},{py}) and ({qx},{qy})")

    def check_five_in_a_row(self, x, y):
        color = self.turn
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1  # Include the current stone
            for direction in [1, -1]:
                nx = x + direction * dx
                ny = y + direction * dy
                while self.in_bounds(nx, ny) and self.board[nx][ny] == color:
                    count += 1
                    nx += direction * dx
                    ny += direction * dy
            if count >= 5:
                return True
        return False

    def check_capture_win(self):
        return self.captures[self.turn] >= 10  # 5 pairs = 10 stones

    def play(self):
        while True:
            self.print_board()
            print(f"\n{self.turn}'s turn.")
            try:
                x, y = map(int, input("Enter move as 'row col' (0-12): ").split())
            except ValueError:
                print("Invalid input format. Please enter numbers in the format 'row col'.")
                continue
            if not self.place_stone(x, y):
                continue
            if self.check_five_in_a_row(x, y):
                self.print_board()
                print(f"{self.turn} wins by five in a row!")
                break
            if self.check_capture_win():
                self.print_board()
                print(f"{self.turn} wins by capturing 5 pairs!")
                break
            self.switch_turn()

if __name__ == "__main__":
    game = PenteGame()
    game.play()
