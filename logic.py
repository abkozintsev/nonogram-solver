import random
import time
from solver import NonogramSolver

class NonogramLogic:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.row_clues = []
        self.col_clues = []
        self.generate_random()

    def generate_random(self):
        # Generates a valid random puzzle
        self.grid = [[random.choice([0, 1]) for _ in range(self.size)] for _ in range(self.size)]
        self.calculate_clues()
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def convert_to_setup(self, player_grid):
        # Uses your drawing as the solution and updates clues
        self.grid = [row[:] for row in player_grid]
        self.calculate_clues()
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def calculate_clues(self):
        self.row_clues = [self._get_line_clues(row) for row in self.grid]
        self.col_clues = [self._get_line_clues([self.grid[r][c] for r in range(self.size)]) for c in range(self.size)]

    def _get_line_clues(self, line):
        clues, count = [], 0
        for cell in line:
            if cell == 1: count += 1
            elif count > 0: clues.append(count); count = 0
        if count > 0: clues.append(count)
        return clues if clues else [0]

    def call_solver(self, current_grid):
        #Executes the solver and measures performance.
        s = NonogramSolver(self.size, self.row_clues, self.col_clues)
        
        start_time = time.perf_counter()
        result = s.solve(current_grid)
        end_time = time.perf_counter()
        
        duration_ms = (end_time - start_time) * 1000
        return result, duration_ms