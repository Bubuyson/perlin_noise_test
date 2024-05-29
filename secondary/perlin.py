import pygame
import noise
import numpy as np
import random
from constants_perlin import *


def generate_terrain(n, m):
    terrain = np.zeros((n, m), dtype=int)
    seed = random.randint(0, MAX_SEED_NUM)  # Random seed for variability

    for i in range(n):
        for j in range(m):
            x = i / SCALE
            y = j / SCALE
            noise_value = noise.pnoise2(x, y, octaves=OCTAVES, persistence=PERSISTANCE,
                                         lacunarity=LACUNARITY, repeatx=REPEAT_X, repeaty=REPEAT_Y, base=seed)
            if noise_value < -0.3:
                terrain[i, j] = 2  # Water
            elif noise_value < 0:
                terrain[i, j] = 1  # Mud
            elif noise_value < 0.4:
                terrain[i, j] = 0  # Grass (more probable)
            elif noise_value < 0.6:
                terrain[i, j] = 3  # Mountain
            else:
                terrain[i, j] = 4  # Resource

    return terrain

def draw_grid(screen, terrain):
    for i in range(N):
        for j in range(M):
            pygame.draw.rect(screen, TERRAIN_COLORS[terrain[i, j]], (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def place_players(terrain):
    # Place players on the grid (bottom-left and top-right corners with some surrounding grass)

    player_positions = [(N-1, 0), (0, M-1)]
    for pos in player_positions:
        terrain[pos[0], pos[1]] = 0  # Ensure grass for player position
        base_size = (random.randint(MIN_BASE_SIZE_X, MAX_BASE_SIZE_X), random.randint(MIN_BASE_SIZE_Y, MAX_BASE_SIZE_Y))
        if base_size[0] > N:
            base_size = (N, base_size[1])
        if base_size[1] > M:
            base_size = (base_size[0], M)

        for dx in range(-1, base_size[0]):
            for dy in range(-1, base_size[1]):
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < N and 0 <= ny < M:
                    terrain[nx, ny] = 0  # Surrounding grass

def main(screen):
    terrain = generate_terrain(N, M)
    place_players(terrain)
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
    
    for _ in range(10):
        # Initialize Pygame
        pygame.init()

        # Initialize screen with dynamic size
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Terrain Generation with Perlin Noise")
        main(screen)
