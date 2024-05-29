import pygame
import noise
import numpy as np
import random
from constants_perlin_new import *
import cv2

def map_terrain_to_numbers(terrain):
    terrain_map = {
        "g": 0,  # Grass
        "m": 1,  # Mud
        "w": 2,  # Water
        "mm": 3,  # Mountain
        "r": 4  # Resource
    }
    return np.vectorize(terrain_map.get)(terrain)


def acceptability_check(terrain):
    # Calculate the variance
    terrain = map_terrain_to_numbers(terrain)
    variance = np.var(terrain)
    
    # Apply edge detection to find straight lines
    edges = cv2.Canny((terrain * 255).astype(np.uint8), 100, 200)
    edge_density = np.sum(edges) / edges.size
    
    return variance, edge_density


def generate_terrain(n, m):
    terrain = np.empty((n, m), dtype=np.str0)
    seed = random.randint(0, MAX_SEED_NUM)  # Random seed for variability

    noise_vals = []
    for i in range(n):
        for j in range(m):
            x = i / SCALE
            y = j / SCALE
            noise_value = noise.pnoise2(x, y, octaves=OCTAVES, persistence=PERSISTANCE,
                                         lacunarity=LACUNARITY, repeatx=REPEAT_X, repeaty=REPEAT_Y, base=seed)
            noise_vals.append(noise_value)
            if noise_value < -0.3:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.0:
                terrain[i, j] = "m"  # Mud
            elif noise_value < 0.05:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.07:
                terrain[i, j] = "mm"  # Mountain
            elif noise_value < 0.4:
                terrain[i, j] = "g"  # Grass (more probable)
            elif noise_value < 0.6:
                terrain[i, j] = "mm"  # Mountain
            else: 
                terrain[i, j] = "g"
                
    return terrain, noise_vals

def generate_terrain2(n, m):
    terrain = np.empty((n, m), dtype=np.str0)
    seed = random.randint(0, MAX_SEED_NUM)  # Random seed for variability

    noise_vals = []
    for i in range(n):
        for j in range(m):
            x = i / SCALE
            y = j / SCALE
            noise_value = noise.pnoise2(x, y, octaves=OCTAVES, persistence=PERSISTANCE,
                                         lacunarity=LACUNARITY, repeatx=REPEAT_X, repeaty=REPEAT_Y, base=seed)
            # noise_value = noise_value * 1.5
            noise_vals.append(noise_value)
            if noise_value < -0.3:
                terrain[i, j] = "w"  # Water
            elif noise_value < -0.12:
                terrain[i, j] = "g"  # Grass
            elif noise_value < -0.1:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.0:
                terrain[i, j] = "m"  # Mud
            elif noise_value < 0.05:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.07:
                terrain[i, j] = "mm"  # Mountain
            elif noise_value < 0.15:
                terrain[i, j] = "g"  # Grass
            elif noise_value < 0.25:
                terrain[i, j] = "m"  # Mud
            elif noise_value < 0.35:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.4:
                terrain[i, j] = "g"  # Grass
            elif noise_value < 0.5:
                terrain[i, j] = "mm"  # Mountain
            elif noise_value < 0.6:
                terrain[i, j] = "m"  # Mud
            else: 
                terrain[i, j] = "g"  # Grass

    return terrain, noise_vals

def draw_grid(screen, terrain):
    for i in range(N):
        for j in range(M):
            pygame.draw.rect(screen, TERRAIN_COLORS[terrain[i, j]], (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def place_players(terrain):
    # Place players on the grid (bottom-left and top-right corners with some surrounding grass)

    base_indexes = set()
    player_positions = [(N-1, 0), (0, M-1)]
    for pos in player_positions:
        terrain[pos[0], pos[1]] = "g"  # Ensure grass for player position
        base_size = (random.randint(MIN_BASE_SIZE_X, MAX_BASE_SIZE_X), random.randint(MIN_BASE_SIZE_Y, MAX_BASE_SIZE_Y))
        if base_size[0] > N:
            base_size = (N, base_size[1])
        if base_size[1] > M:
            base_size = (base_size[0], M)

        
        for dx in range(-1, base_size[0]):
            for dy in range(-1, base_size[1]):
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < N and 0 <= ny < M:
                    terrain[nx, ny] = "g"  # Surrounding grass
                    base_indexes.add((nx, ny))

    return base_indexes

def place_rewards(terrain, base_indexes):
    num_clusters = random.randint(1, NUM_CLUSTER)  # Number of reward clusters
    rewards = []
    
    # Flatten base_indexes list for easier checking
    base_positions = set(base_indexes)
    
    for _ in range(num_clusters):
        cluster_size = random.randint(MIN_REWARD_SIZE, MAX_REWARD_SIZE)
        n_trials = 0
        while True and n_trials < 100:
            # Find a grassy area to start the cluster
            cluster_y, cluster_x = random.randint(0, len(terrain)-1), random.randint(0, len(terrain[0])-1)
            n_trials += 1
            if terrain[cluster_y][cluster_x] == 'g':
                break
        
        # Place the cluster around the starting point, ensuring all are on grass
        for _ in range(cluster_size):
            offset_y, offset_x = random.randint(-1, 1), random.randint(-1, 1)
            reward_y, reward_x = cluster_y + offset_y, cluster_x + offset_x
            if (reward_y, reward_x) not in base_positions and 0 <= reward_y < len(terrain) and 0 <= reward_x < len(terrain[0]) and terrain[reward_y][reward_x] == 'g':
                rewards.append({'x': reward_x, 'y': reward_y})
                terrain[reward_y][reward_x] = 'r'
    
    return rewards



def main(screen):
    terrain, noise_vals = generate_terrain2(N, M)
    
    # print noise vals for 3 digits
    # print("Noise values: ", [round(x, 3) for x in noise_vals])

    base_indexes = place_players(terrain)
    place_rewards(terrain, base_indexes)

    var, edge_density = acceptability_check(terrain)

    print(f"Variance: {var}, Edge Density: {edge_density}")
    if var > VARIANCE_LIMIT and edge_density > EDGE_LIMIT:
        print("Noise is acceptable.")

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
