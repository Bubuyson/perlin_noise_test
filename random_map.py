
import pygame
import noise
import numpy as np
import random


# Constants.py

# Size of each grid cell
GRID_SIZE = 50  

# Number of grid cells in y direction
N = 18
# Number of grid cells in x direction
M = 24


# Dynamically set window size based on grid dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = M * GRID_SIZE, N * GRID_SIZE

# Terrain types with distinct colors
TERRAIN_COLORS = {
    0: (34, 139, 34),  # Grass
    1: (139, 69, 19),  # Mud
    2: (0, 0, 255),    # Water
    3: (169, 169, 169),# Mountain
    4: (255, 215, 0)   # Resource
}
BACKGROUND_COLOR = (0, 0, 0)  # Black background color

SCALE = 10.0  # Adjust scale for smoother transitions
OCTAVES = 10  # Number of levels of detail
PERSISTANCE = 0.5  # Amplitude of each octave
LACUNARITY = 2.0  # Frequency of each octave

REPEAT_X = N  # Repeat noise pattern in x direction
REPEAT_Y = M  # Repeat noise pattern in y direction

MAX_SEED_NUM = 1e4

MIN_BASE_SIZE_X = 2
MIN_BASE_SIZE_Y = 2
MAX_BASE_SIZE_X = 5
MAX_BASE_SIZE_Y = 5



def generate_terrain(n, m):
    terrain = np.empty((n, m), dtype=np.str0)
    seed = random.randint(0, MAX_SEED_NUM)  # Random seed for variability

    for i in range(n):
        for j in range(m):
            x = i / SCALE
            y = j / SCALE
            noise_value = noise.pnoise2(x, y, octaves=OCTAVES, persistence=PERSISTANCE,
                                         lacunarity=LACUNARITY, repeatx=REPEAT_X, repeaty=REPEAT_Y, base=seed)
            if noise_value < -0.3:
                terrain[i, j] = "w"  # Water
            elif noise_value < 0.0:
                terrain[i, j] = "m"  # Mud
            elif noise_value < 0.4:
                terrain[i, j] = "g"  # Grass (more probable)
            elif noise_value < 0.6:
                terrain[i, j] = "m"  # Mountain
            else: 
                terrain[i, j] = "g"
                
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
                    terrain[nx, ny] = "g"  # Surrounding grass



def place_units(terrain, team_color):
    units = []
    unit_types = ['Truck', 'Light Tank', 'Heavy Tank', 'Drone']
    num_units = random.randint(3, 6)  # Random number of units
    base_x, base_y = random.randint(0, len(terrain[0])-1), random.randint(0, len(terrain)-1)
    
    # Place the base
    base = {'base': {'x': base_x, 'y': base_y}, 'units': []}
    
    # Place the units near the base
    for _ in range(num_units):
        unit_type = random.choice(unit_types)
        # Ensure units are placed near the base, within boundaries
        unit_x = max(0, min(len(terrain[0])-1, base_x + random.randint(-1, 1)))
        unit_y = max(0, min(len(terrain)-1, base_y + random.randint(-1, 1)))
        base['units'].append({'type': unit_type, 'x': unit_x, 'y': unit_y})
    
    return base

def place_rewards(terrain):
    num_clusters = random.randint(1, 3)  # Number of reward clusters
    rewards = []
    
    for _ in range(num_clusters):
        cluster_size = random.randint(3, 5)  # Number of rewards per cluster
        while True:
            # Find a grassy area to start the cluster
            cluster_x, cluster_y = random.randint(0, len(terrain[0])-1), random.randint(0, len(terrain)-1)
            if terrain[cluster_y][cluster_x] == 'g':
                break
        
        # Place the cluster around the starting point, ensuring all are on grass
        for _ in range(cluster_size):
            offset_x, offset_y = random.randint(-1, 1), random.randint(-1, 1)
            reward_x, reward_y = cluster_x + offset_x, cluster_y + offset_y
            if 0 <= reward_x < len(terrain[0]) and 0 <= reward_y < len(terrain) and terrain[reward_y][reward_x] == 'g':
                rewards.append({'x': reward_x, 'y': reward_y})
    
    return rewards


def generate_random_map():
    # Prepare the map dictionary structure
    
    terrain = generate_terrain(N,M)
    
    map_config = {
        'max_turn': 5000,
        'turn_timer': 2,
        'map': {
            'x': len(terrain[0]),
            'y': len(terrain),
            'terrain': [list(row) for row in terrain]
        },
        'red': place_units(terrain, 'red'),
        'blue': place_units(terrain, 'blue'),
        'resources': place_rewards(terrain)
    }
    return map_config

