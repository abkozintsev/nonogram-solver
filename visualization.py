import pygame

class NonogramViz:
    def __init__(self, screen, size):
        self.screen, self.size, self.cell = screen, size, 40
        self.ox, self.oy = 180, 180
        self.font = pygame.font.SysFont('Arial', 14)
        pygame.display.set_caption("Nonogram Solver")


    def draw(self, player_grid, logic):
        self.screen.fill((255, 255, 255))
        is_won = all(logic._get_line_clues(player_grid[r]) == logic.row_clues[r] for r in range(self.size))
        
        # Draw Row Clues (Horizontal)
        for r, clues in enumerate(logic.row_clues):
            row_match = logic._get_line_clues(player_grid[r]) == clues
            txt = self.font.render(" ".join(map(str, clues)), True, (0,150,0) if row_match else (0,0,0))
            self.screen.blit(txt, (self.ox - txt.get_width() - 10, self.oy + r*self.cell + 12))

        # Draw Column Clues (Vertical)
        for c, clues in enumerate(logic.col_clues):
            col_data = [player_grid[r][c] for r in range(self.size)]
            col_match = logic._get_line_clues(col_data) == clues
            color = (0,150,0) if col_match else (0,0,0)
            for i, val in enumerate(reversed(clues)):
                txt = self.font.render(str(val), True, color)
                self.screen.blit(txt, (self.ox + c*self.cell + 15, self.oy - (i+1)*20 - 5))

        # Draw Grid
        for r in range(self.size):
            for c in range(self.size):
                rect = pygame.Rect(self.ox + c*self.cell, self.oy + r*self.cell, self.cell, self.cell)
                if player_grid[r][c] == 1:
                    pygame.draw.rect(self.screen, (255,0,0) if is_won else (0,0,0), rect)
                elif player_grid[r][c] == 2: # Clear/X
                    # Draw a small gray square or X in the middle
                    small_rect = rect.inflate(-20, -20)
                    pygame.draw.rect(self.screen, (180, 180, 180), small_rect)

                pygame.draw.rect(self.screen, (200,200,200), rect, 1)

    def get_buttons(self):
        btn_data = [("Random", 20), ("Set Pattern", 140), ("Solve", 260)]
        rects = []
        for text, x in btn_data:
            r = pygame.Rect(x, 580, 100, 40)
            pygame.draw.rect(self.screen, (100, 100, 100), r)
            self.screen.blit(self.font.render(text, True, (255,255,255)), (x+10, 590))
            rects.append(r)
        return rects