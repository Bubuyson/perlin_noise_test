# Constants.py

# Size of each grid cell
GRID_SIZE = 50  

# Number of grid cells in y direction
N = 15
# Number of grid cells in x direction
M = 7


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

