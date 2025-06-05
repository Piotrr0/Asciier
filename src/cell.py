class Cell:
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.revealed = False
        self.flagged = False

    def __str__(self):
        if self.flagged:
            return "F"
        if not self.revealed:
            return "*"
        if self.is_mine:
            return "X"
        return str(self.adjacent_mines) if self.adjacent_mines > 0 else " "