import pygame
import numpy as np
from constants_manual import *

def generate_terrain_from_manual_map(manual_map):
    n, m = len(manual_map), len(manual_map[0])
    terrain = np.empty((n, m), dtype=str)

    for i in range(n):
        for j in range(m):
            terrain[i, j] = manual_map[i][j]

    return terrain

def draw_grid(screen, terrain):
    n, m = terrain.shape
    for i in range(n):
        for j in range(m):
            pygame.draw.rect(screen, TERRAIN_COLORS[terrain[i, j]], (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main(screen, manual_map):
    terrain = generate_terrain_from_manual_map(manual_map)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, terrain)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    manual_map = MANUAL_MAP1

    # Initialize Pygame
    pygame.init()

    # Determine the size of the grid based on the manual map
    N = len(manual_map)
    M = len(manual_map[0])

    # Dynamically set window size based on grid dimensions
    WINDOW_WIDTH, WINDOW_HEIGHT = M * GRID_SIZE, N * GRID_SIZE

    # Initialize screen with dynamic size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Manual Terrain Map")
    main(screen, manual_map)
