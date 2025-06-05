from board import Board

class Asciier:
    def __init__(self, width=10, height=10, mines=15):
        self.board = Board(width, height)
        self.mines = mines
        self.game_over = False
        self.won = False

    def play(self):
        self.print_instructions()
        
        while not self.game_over:
            self.board.draw_board()
            if self.board.first_click:
                print("Make your first move to start the game!")

            command = self.get_user_command()
            if command is None:
                continue
            
            action, x, y = command
            self.handle_action(action, x, y)

    def print_instructions(self):
        print("Commands:")
        print("  r x y - Reveal cell at position (x, y)")
        print("  f x y - Flag/unflag cell at position (x, y)")
        print("  q     - Quit game")
        print()

    def get_user_command(self):
        try:
            raw_input = input("Enter command: ").strip().lower().split()
            if not raw_input:
                return None

            if raw_input[0] == 'q':
                print("Thanks for playing!")
                self.game_over = True
                return None

            if len(raw_input) != 3:
                print("Invalid command format. Use 'r x y' or 'f x y'")
                return None

            try:
                x, y = int(raw_input[1]), int(raw_input[2])
            except ValueError:
                print("Invalid coordinates. Please enter numbers.")
                return None

            if not (0 <= x < self.board.width and 0 <= y < self.board.height):
                print(f"Coordinates out of bounds. Valid range: 0-{self.board.width - 1}, 0-{self.board.height - 1}")
                return None

            return raw_input[0], x, y

        except KeyboardInterrupt:
            print("\nGame interrupted. Thanks for playing!")
            self.game_over = True
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def handle_action(self, action, x, y):
        if action == 'r':
            self.reveal(x, y)
        elif action == 'f':
            self.board.toggle_flag(x, y)
        else:
            print("Invalid command. Use 'r' to reveal or 'f' to flag.")

    def reveal(self, x, y):
        if self.board.first_click:
            self.board.create_mine_board(self.mines, x, y)
            self.board.first_click = False

        hit_mine = self.board.reveal_cell(x, y)

        if hit_mine:
            self.end_game(lost=True)
        elif self.board.is_won():
            self.end_game(won=True)

    def end_game(self, won=False, lost=False):
        self.game_over = True
        self.won = won

        if lost:
            self.board.reveal_all_mines()

        self.board.draw_board()
        if won:
            print("You won!")
        elif lost:
            print("You hit a mine! Game Over!")