import pygame
import numpy as np

# Constants
cell_size = 10
grid_color = (150, 150, 150)
alive = (255, 255, 0)
bg_color = (0, 0, 0)

def create_grid(rows, cols):
    return np.zeros((rows, cols), dtype=bool)

def draw_grid(screen, grid):    
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            if grid[row, col]:
                # Alive cell
                pygame.draw.rect(screen, alive, (col * cell_size, row * cell_size, cell_size, cell_size))
            else:
                # Dead cell
                pygame.draw.rect(screen, bg_color, (col * cell_size, row * cell_size, cell_size, cell_size))

def update_grid(grid):
    rows, cols = grid.shape
    new_grid = grid.copy()
    
    for row in range(rows):
        for col in range(cols):
            # Counting number of live cells
            neighbors = np.sum(grid[max(row - 1, 0):min(row + 2, rows), max(col - 1, 0):min(col + 2, cols)]) - grid[row, col]
            
            # Overpopulated and Underpopulated
            if grid[row, col] and (neighbors < 2 or neighbors > 3):
                new_grid[row, col] = False
            
            # Regeneration of Dead cell if 3 neighbours
            elif not grid[row, col] and neighbors == 3:
                new_grid[row, col] = True
    
    return new_grid

def main():
    pygame.init()

    # Seting up the screen
    rows, cols = 120, 120
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of Life")

    # Initial grid
    grid = create_grid(rows, cols)
    init_grid = grid.copy()

    # Game loop
    running = True
    paused = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Pausing and Unpausing the game
                if event.key == pygame.K_SPACE:
                    paused = not paused
        
                # Escape to Stop the game incase the quit button is unreachable xD
                elif event.key == pygame.K_ESCAPE:
                    running = False

                # Clearing the board
                elif event.key == pygame.K_c:
                    grid = create_grid(rows, cols)
                
                # Randomly filling the board (30% probability of cell being alive)
                elif event.key == pygame.K_e:
                    grid = np.random.choice([False, True], size=(rows, cols), p=[0.6, 0.4])
            
                # Resets to last set board:
                elif event.key == pygame.K_r:
                    grid = init_grid

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not paused:
                    continue
                # Getting mouse cords
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // cell_size
                row = mouse_pos[1] // cell_size
                if 0 <= row < rows and 0 <= col < cols:
                    # Reversing the current cell state on click
                    grid[row, col] = not grid[row, col]
                init_grid = grid
        # Update the grid
        if not paused:
            grid = update_grid(grid)

        # Draw the grid
        draw_grid(screen, grid)

        # Draw grid lines
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, grid_color, (0, y), (width, y))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(10)

    # Quit the game
    pygame.quit()

main()
