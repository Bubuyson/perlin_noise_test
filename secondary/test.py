import numpy as np
import matplotlib.pyplot as plt
import cv2

# Define a structured numpy array (2D grid) with a regular pattern
def generate_structured_grid(shape):
    grid = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            grid[i, j] = (i + j) % 2  # Alternating pattern
    return grid


def random_shape():
    # Define a numpy array (2D grid) with random values
    shape = (100, 100)
    noise_level = 0.5  # Adjust this to control the noise intensity
    grid = np.random.rand(*shape) * noise_level
    return grid

def check_noise_quality(noise_grid):
    # Calculate the variance
    variance = np.var(noise_grid)
    
    # Apply edge detection to find straight lines
    edges = cv2.Canny((noise_grid * 255).astype(np.uint8), 100, 200)
    edge_density = np.sum(edges) / edges.size
    
    return variance, edge_density

grid = random_shape()
# Check the quality of the noise
variance, edge_density = check_noise_quality(grid)
print(f"Variance of random: {variance}, Edge Density of random: {edge_density}")

grid2 = generate_structured_grid((100, 100))
# Check the quality of the noise
variance, edge_density = check_noise_quality(grid2)
print(f"Variance of structured: {variance}, Edge Density of structured: {edge_density}")

# Determine if the noise is acceptable
if variance > 0.3 and edge_density > 0.3:
    print("Noise is acceptable.")
else:
    print("Noise is not acceptable.")

# Optional: Visualize the noisy grid
plt.imshow(grid, cmap='gray')
plt.title("Noisy Grid")
plt.colorbar()
plt.show()
