import random


class Board():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.total_cells = self.width * self.height
        self.cells = [''] * (self.total_cells)
        self.visual_cells = ['*'] * (self.total_cells)
        self.create_mine_board(20, 2, 2)
        
        
    def get_cell(self, x: int, y: int):
        return self.cells[y * self.width + x]

    def draw_board(self):
        for y in range(self.height):
            row = self.cells[y * self.width:(y + 1) * self.width]
            print(' '.join(row))

    def generate_mines(self, mines_count: int, safe_x: int, safe_y: int, safe_radius=2):
        if mines_count > self.total_cells - ((2 * safe_radius + 1) ** 2):
            raise ValueError("Too many mines for the board size excluding safe area.")

        safe_positions = set()

        for dy in range(-safe_radius, safe_radius + 1):
            for dx in range(-safe_radius, safe_radius + 1):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_positions.add(ny * self.width + nx)

        possible_positions = [i for i in range(self.total_cells) if i not in safe_positions]
        mine_positions = random.sample(possible_positions, mines_count)

        for pos in mine_positions:
            self.cells[pos] = 'M'
        

    def calculate_adjacent_mines(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1), (1, -1),
                (1, 0), (1, 1)]
    
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                if self.cells[index] == 'M':
                    continue
            
                count = 0
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        n_index = ny * self.width + nx
                        if self.cells[n_index] == 'M':
                            count += 1
                self.cells[index] = str(count) if count > 0 else ' '

    def create_mine_board(self, mines_count: int, save_x: int, save_y: int):
        self.generate_mines(mines_count, save_x, save_y)
        self.calculate_adjacent_mines()