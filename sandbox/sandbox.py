import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === 1. Define Parameters ===
grid_rows, grid_cols = 3, 3  # Arrange simulations in a 3x3 grid
num_frames = 100  # Number of animation frames

# Create random initial states for demonstration (Replace with real double pendulum data)
grid_states = np.random.rand(num_frames, grid_rows, grid_cols, 10, 10)  # (frames, rows, cols, grid_height, grid_width)

# === 2. Create Figure and Subplots ===
fig, axes = plt.subplots(grid_rows, grid_cols, figsize=(8, 8))  # 3x3 grid of subplots
images = []

for i in range(grid_rows):
    for j in range(grid_cols):
        ax = axes[i, j]
        im = ax.imshow(grid_states[0, i, j], cmap='inferno', vmin=0, vmax=1)
        images.append(im)
        ax.set_xticks([])  # Remove x ticks
        ax.set_yticks([])  # Remove y ticks

# === 3. Define Update Function ===
def update(frame):
    for idx, im in enumerate(images):
        i, j = divmod(idx, grid_cols)  # Convert index to (row, col)
        im.set_array(grid_states[frame, i, j])  # Update each subplot's grid
    return images  # Return updated images

# === 4. Create Animation ===
ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=100)
ani.save("test.mp4", fps=30, writer="ffmpeg")

# === 5. Show Animation ===
plt.close()
