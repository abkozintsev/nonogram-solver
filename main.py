import pygame
from logic import NonogramLogic
from visualization import NonogramViz

def main():
    pygame.init()
    size = 9
    screen = pygame.display.set_mode((750, 700))
    logic = NonogramLogic(size)
    viz = NonogramViz(screen, size)
    player_grid = [[0 for _ in range(size)] for _ in range(size)]
    
    dragging = False
    drag_val = 0
    clock = pygame.time.Clock()
    while True:
        viz.draw(player_grid, logic)
        btn_rand, btn_set, btn_solve = viz.get_buttons()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if btn_rand.collidepoint(pos):
                    player_grid = logic.generate_random()
                elif btn_set.collidepoint(pos):
                    player_grid = logic.convert_to_setup(player_grid)
                elif btn_solve.collidepoint(pos):
                    res, t = logic.call_solver(player_grid)
                    if res:
                        player_grid = res
                        print(f"Solved in {t:.2f}ms")
                    else:
                        print("Contradiction found!")
                else:
                    gx, gy = (pos[0] - viz.ox)//viz.cell, (pos[1] - viz.oy)//viz.cell
                    if 0 <= gx < size and 0 <= gy < size:
                        dragging = True
                        # Determine what value we are painting with
                        target = 1 if event.button == 1 else 2
                        drag_val = target if player_grid[gy][gx] != target else 0
                        player_grid[gy][gx] = drag_val

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                pos = pygame.mouse.get_pos()
                gx, gy = (pos[0] - viz.ox)//viz.cell, (pos[1] - viz.oy)//viz.cell
                if 0 <= gx < size and 0 <= gy < size:
                    player_grid[gy][gx] = drag_val
        clock.tick(60)

if __name__ == "__main__": main()