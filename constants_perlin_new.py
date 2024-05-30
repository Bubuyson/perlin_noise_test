# Constants.py

# Size of each grid cell
GRID_SIZE = 30

# Number of grid cells in y direction
N = 18
# Number of grid cells in x direction
M = 24

GRASS_CODE    = 'g'
MUD_CODE      = 'm'
WATER_CODE    = 'w'
MOUNTAIN_CODE = 'd'
RESOURCE_CODE = 'r'

# Dynamically set window size based on grid dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = M * GRID_SIZE, N * GRID_SIZE

# Terrain types with distinct colors
TERRAIN_COLORS = {
    GRASS_CODE    : (34, 139, 34),  # Grass
    MUD_CODE      : (139, 69, 19),  # Mud
    WATER_CODE    : (0, 0, 255),    # Water
    MOUNTAIN_CODE : (169, 169 , 169),# Mountain
    RESOURCE_CODE : (255, 215, 0)   # Resource
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

# Reward clusters

# NUM_CLUSTER = N*M//50
NUM_CLUSTER = 5
MIN_CLUSTER_SIZE = 5
MAX_CLUSTER_SIZE = 5
MAX_OFFSET_TEST = 5


VARIANCE_LIMIT = 0.45
EDGE_DENSITY_LIMIT = 45

MAX_NUM_TRIAL_FOR_RESOURCE = 30
MAX_NUM_FOR_CLUSTER_FIND = 100
