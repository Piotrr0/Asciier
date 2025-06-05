import random
from cell import Cell

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.total_cells = self.width * self.height
        self.cells = [Cell() for _ in range(self.total_cells)]
        self.mines_count = 0
        self.first_click = True
        self.direction = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),          (0, 1),
                          (1, -1), (1, 0),  (1, 1)]

    def get_index(self, x: int, y: int):
        return y * self.width + x

    def draw_indices(self):
        print("   ", end="")
        for x in range(self.width):
            print(f"{x:2d}", end=" ")
        print()

    def draw_board(self):
        self.draw_indices()
        for y in range(self.height):
            print(f"{y:2d} ", end="")
            for x in range(self.width):
                index = self.get_index(x, y)
                print(f" {self.cells[index]}", end=" ")
            print()
        print()

    def generate_mines(self, mines_count: int, safe_x: int, safe_y: int, safe_radius=1):
        if mines_count > self.total_cells - ((2 * safe_radius + 1) ** 2):
            raise ValueError("Too many mines for the board size excluding safe area.")

        safe_positions = set()
        for dy in range(-safe_radius, safe_radius + 1):
            for dx in range(-safe_radius, safe_radius + 1):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_positions.add(self.get_index(nx, ny))

        possible_positions = [i for i in range(self.total_cells) if i not in safe_positions]
        mine_positions = random.sample(possible_positions, mines_count)

        for pos in mine_positions:
            self.cells[pos].is_mine = True

        self.mines_count = mines_count

    def calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                index = self.get_index(x, y)
                cell = self.cells[index]
                if cell.is_mine:
                    continue

                count = 0
                for dx, dy in self.direction:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor = self.cells[self.get_index(nx, ny)]
                        if neighbor.is_mine:
                            count += 1
                cell.adjacent_mines = count

    def create_mine_board(self, mines_count: int, safe_x: int, safe_y: int):
        self.generate_mines(mines_count, safe_x, safe_y)
        self.calculate_adjacent_mines()

    def reveal_cell(self, x: int, y: int):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        index = self.get_index(x, y)
        cell = self.cells[index]
        if cell.revealed or cell.flagged:
            return False

        cell.revealed = True

        if cell.is_mine:
            return True

        if cell.adjacent_mines == 0:
            self.reveal_adjacent(x, y)

        return False

    def reveal_adjacent(self, x: int, y: int):
        for dx, dy in self.direction:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                index = self.get_index(nx, ny)
                neighbor = self.cells[index]
                if not neighbor.revealed and not neighbor.flagged:
                    neighbor.revealed = True
                    if neighbor.adjacent_mines == 0 and not neighbor.is_mine:
                        self.reveal_adjacent(nx, ny)

    def toggle_flag(self, x: int, y: int):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        index = self.get_index(x, y)
        cell = self.cells[index]
        if not cell.revealed:
            cell.flagged = not cell.flagged

    def is_won(self):
        for cell in self.cells:
            if not cell.is_mine and not cell.revealed:
                return False
        return True

    def reveal_all_mines(self):
        for cell in self.cells:
            if cell.is_mine:
                cell.revealed = True