import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Simulation settings
star_pos = np.array([0, 0])  # Star at the center
planet_dist = 1  # Distance of the planet from the star
planet_speed = 0.02  # Speed of planet in radians per frame
num_frames = 500

# Create the plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# Draw the star
star = plt.Circle(star_pos, 0.2, color='yellow', zorder=1)
ax.add_artist(star)

# Draw the coronagraph (dark circle)
coronagraph = plt.Circle(star_pos, 0.3, color='black', zorder=2)
ax.add_artist(coronagraph)

# Draw the planet
planet, = ax.plot([], [], 'ro', markersize=5, zorder=3)


# Update function for the animation
def update(frame):
    # Calculate planet position
    angle = planet_speed * frame
    planet_x = planet_dist * np.cos(angle)
    planet_y = planet_dist * np.sin(angle)

    # Update planet position
    planet.set_data(planet_x, planet_y)
    return planet,


# Animation loop
for frame in range(num_frames):
    update(frame)
    plt.pause(0.01)

plt.show()
