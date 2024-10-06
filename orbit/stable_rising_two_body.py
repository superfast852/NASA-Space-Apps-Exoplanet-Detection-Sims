import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_earth = 5.972e24  # Mass of body 1 (kg) - e.g., Earth
M_moon = 7.348e22  # Mass of body 2 (kg) - e.g., Moon
dt = 10000  # Time step (s)
steps = 1000  # Number of simulation steps

# Initial positions (m)
r1 = np.array([0, 0, 0], dtype=float)  # Position of body 1 (earth)
r2 = np.array([384.4e6, 0, 0], dtype=float)  # Position of body 2 (e.g., distance from Earth to Moon)

# Initial velocities (m/s)
v1 = np.array([0, 0, 150], dtype=float)  # Initial velocity of body 1
v2 = np.array([0, 1022, 0], dtype=float)  # Initial velocity of body 2

# Function to calculate the gravitational force
def gravitational_force(r1, r2):
    r = r2 - r1
    dist = np.linalg.norm(r)
    force = G * M_earth * M_moon / dist ** 2
    direction = r / dist
    return force * direction

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot initial positions
body1_plot, = ax.plot([r1[0]], [r1[1]], [r1[2]], 'bo', label='Body 1')
body2_plot, = ax.plot([r2[0]], [r2[1]], [r2[2]], 'ro', label='Body 2')

# Set plot limits and labels
ax.set_xlim([-5e8, 5e8])
ax.set_ylim([-5e8, 5e8])
ax.set_zlim([-5e8, 5e8])
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Live Two-Body Orbit Simulation in 3D')
ax.legend()
ctr = 0
pt_count = 20

# Simulation loop
for _ in range(steps):
    # Compute forces
    F12 = gravitational_force(r1, r2)
    F21 = -F12

    # Update velocities
    v1 += F12 / M_earth * dt
    v2 += F21 / M_moon * dt

    # Update positions
    r1 += v1 * dt
    r2 += v2 * dt

    # Update the plot data
    body1_plot.set_data([r1[0]], [r1[1]])
    body1_plot.set_3d_properties([r1[2]])
    body2_plot.set_data([r2[0]], [r2[1]])
    body2_plot.set_3d_properties([r2[2]])
    if ctr % pt_count == 0:
        ax.scatter(r1[0], r1[1], r1[2], 'b+')
        ax.scatter(r2[0], r2[1], r2[2], 'r+')
        ctr = 0
    ctr += 1
    # Redraw the plot with a small pause
    plt.pause(0.00001)

plt.show()
