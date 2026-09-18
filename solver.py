import copy

class NonogramSolver:
    def __init__(self, size, row_clues, col_clues):
        self.size = size
        self.row_clues, self.col_clues = row_clues, col_clues
        self.memo = {}

    def get_possibilities(self, clues, current_line):
        line_tuple = tuple(current_line)
        clue_tuple = tuple(clues)
        if (clue_tuple, line_tuple) in self.memo:
            return self.memo[(clue_tuple, line_tuple)]

        n = len(current_line)
        def generate(c_idx, start_pos):
            if c_idx == len(clues):
                if any(current_line[i] == 1 for i in range(start_pos, n)): return []
                return [[2] * (n - start_pos)]
            
            res = []
            needed = sum(clues[c_idx:]) + len(clues) - c_idx - 1
            for i in range(start_pos, n - needed + 1):
                if any(current_line[j] == 1 for j in range(start_pos, i)): continue # Blocked by existing black
                if any(current_line[j] == 2 for j in range(i, i + clues[c_idx])): continue # Blocked by existing white
                
                block = [2] * (i - start_pos) + [1] * clues[c_idx]
                sep = i + clues[c_idx]
                
                if sep < n:
                    if current_line[sep] == 1: continue
                    for rest in generate(c_idx + 1, sep + 1):
                        res.append(block + [2] + rest)
                else:
                    for rest in generate(c_idx + 1, sep):
                        res.append(block + rest)
            return res

        result = generate(0, 0)
        self.memo[(clue_tuple, line_tuple)] = result
        return result

    def deduce(self, grid):
        changed = True
        while changed:
            changed = False
            # Check Rows
            for r in range(self.size):
                poss = self.get_possibilities(self.row_clues[r], grid[r])
                if not poss: return None
                for c in range(self.size):
                    if grid[r][c] == 0:
                        first_val = poss[0][c]
                        if all(p[c] == first_val for p in poss):
                            grid[r][c] = first_val
                            changed = True
            # Check Columns
            for c in range(self.size):
                col = [grid[r][c] for r in range(self.size)]
                poss = self.get_possibilities(self.col_clues[c], col)
                if not poss: return None
                for r in range(self.size):
                    if grid[r][c] == 0:
                        first_val = poss[0][r]
                        if all(p[r] == first_val for p in poss):
                            grid[r][c] = first_val
                            changed = True
        return grid

    def solve(self, grid):
        # Treat all 0s as 'unknown' for deduction
        grid = self.deduce(grid)
        if grid is None: return None
        
        # Check if complete
        if all(cell != 0 for row in grid for cell in row):
            return grid

        # Find first unknown and guess
        for r in range(self.size):
            for c in range(self.size):
                if grid[r][c] == 0:
                    for val in [1, 2]:
                        test_grid = copy.deepcopy(grid)
                        test_grid[r][c] = val
                        res = self.solve(test_grid)
                        if res: return res
                    return None
        return None