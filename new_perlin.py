import pygame
import noise
import numpy as np
import random
from constants_perlin_new import *
import os
import cv2

os.environ['SDL_VIDEO_WINDOW_POS'] = "700,400"

def map_terrain_to_numbers(terrain):
    terrain_map = {
        GRASS_CODE: 0,  # Grass
        MUD_CODE: 1,  # Mud
        WATER_CODE: 2,  # Water
        MOUNTAIN_CODE: 3,  # Mountain
        RESOURCE_CODE: 4  # Resource
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
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < 0.0:
                terrain[i, j] = MUD_CODE  # Mud
            elif noise_value < 0.05:
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < 0.07:
                terrain[i, j] = MOUNTAIN_CODE  # Mountain
            elif noise_value < 0.4:
                terrain[i, j] = GRASS_CODE  # Grass (more probable)
            elif noise_value < 0.6:
                terrain[i, j] = MOUNTAIN_CODE  # Mountain
            else: 
                terrain[i, j] = GRASS_CODE
                
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
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < -0.12:
                terrain[i, j] = GRASS_CODE  # Grass
            elif noise_value < -0.1:
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < 0.0:
                terrain[i, j] = MUD_CODE  # Mud
            elif noise_value < 0.05:
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < 0.07:
                terrain[i, j] = MOUNTAIN_CODE  # Mountain
            elif noise_value < 0.15:
                terrain[i, j] = GRASS_CODE  # Grass
            elif noise_value < 0.25:
                terrain[i, j] = MUD_CODE  # Mud
            elif noise_value < 0.35:
                terrain[i, j] = WATER_CODE  # Water
            elif noise_value < 0.4:
                terrain[i, j] = GRASS_CODE  # Grass
            elif noise_value < 0.5:
                terrain[i, j] = MOUNTAIN_CODE  # Mountain
            elif noise_value < 0.6:
                terrain[i, j] = MUD_CODE  # Mud
            else: 
                terrain[i, j] = GRASS_CODE  # Grass

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
        terrain[pos[0], pos[1]] = GRASS_CODE  # Ensure grass for player position
        base_size = (random.randint(MIN_BASE_SIZE_X, MAX_BASE_SIZE_X + 1), random.randint(MIN_BASE_SIZE_Y, MAX_BASE_SIZE_Y + 1))
        if base_size[0] > N:
            base_size = (N, base_size[1])
        if base_size[1] > M:
            base_size = (base_size[0], M)

        
        for dx in range(-1, base_size[0]):
            for dy in range(-1, base_size[1]):
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < N and 0 <= ny < M:
                    terrain[nx, ny] = GRASS_CODE  # Surrounding grass
                    base_indexes.add((nx, ny))

    return base_indexes

def place_rewards(terrain, base_positions):
    num_clusters = NUM_CLUSTER  # Number of reward clusters
    resources = []
    total_trial = 0
    i = 0
    while i < num_clusters and total_trial <= MAX_NUM_TRIAL_FOR_RESOURCE:
        cluster_size = random.randint(MIN_CLUSTER_SIZE, MAX_CLUSTER_SIZE)
        n_trials = 0
        while True and n_trials <= MAX_NUM_FOR_CLUSTER_FIND:
            # Find a grassy area to start the cluster
            cluster_y, cluster_x = random.randint(0, len(terrain)-1), random.randint(0, len(terrain[0])-1)
            n_trials += 1
            if terrain[cluster_y][cluster_x] not in [MOUNTAIN_CODE, RESOURCE_CODE] and (cluster_y, cluster_x) not in base_positions and 0 <= cluster_y < len(terrain) and 0 <= cluster_x < len(terrain[0]):
                break
        
        # Place the cluster around the starting point, ensuring all are on grass
        that_cluster_list = set()
        that_cluster_list.add((cluster_y, cluster_x))
        resource_put = False
        first_offset = True
        for k in range(0, cluster_size):
            offset_trial = 0
            offset_done = False
            while offset_trial <= MAX_OFFSET_TEST and not offset_done:
                if first_offset:
                    offset_x = offset_y = 0
                    
                else:
                    offset_y, offset_x = np.random.randint(-1, 2), np.random.randint(-1, 2)
                    if offset_x == offset_y or offset_x == -offset_y:
                        if np.random.randint(2):
                            offset_y = 0
                        else:
                            offset_x = 0
                
                sampled_cluster_point = random.sample(sorted(that_cluster_list), 1)[0]
                reward_y, reward_x = sampled_cluster_point[0] + offset_y, sampled_cluster_point[1] + offset_x
                
                if first_offset or ((reward_y, reward_x) not in that_cluster_list and (reward_y, reward_x) not in base_positions and 0 <= reward_y < len(terrain) and 0 <= reward_x < len(terrain[0])): #and terrain[reward_y][reward_x] is not 'mm':
                    resources.append({'x': reward_x, 'y': reward_y})
                    that_cluster_list.add((reward_y, reward_x))
                    terrain[reward_y][reward_x] = RESOURCE_CODE
                    resource_put = True
                    offset_done = True
                    first_offset = False
                    
                offset_trial += 1
        if resource_put:
            i += 1
        total_trial += 1
                
    
    return resources



def main(screen):
    terrain, noise_vals = generate_terrain2(N, M)
    # terrain, noise_vals = generate_terrain(N, M)
    
    # print noise vals for 3 digits
    # print("Noise values: ", [round(x, 3) for x in noise_vals])

    base_indexes = place_players(terrain)
    var, edge_density = acceptability_check(terrain)
    
    print(f"Variance is {var},", end=" ") 
    print(f"edge density is {edge_density}")
    if var > VARIANCE_LIMIT:
        print("Variance is acceptable.")
    else:
        print("Variance is not acceptable")

    
    if edge_density > EDGE_DENSITY_LIMIT:
        print("Edge density is acceptable.")
    else:
        print("Edge density is not acceptable.")
        
    rewards = place_rewards(terrain, base_indexes)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, terrain)
        pygame.display.flip()
        a = 1

    pygame.quit()


if __name__ == "__main__":
    
    for i in range(10):
        
        # Initialize Pygame
        pygame.init()

        # Initialize screen with dynamic size
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Terrain Generation with Perlin Noise")
        main(screen)
