import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M1 = 5.972e24  # Mass of body 1 (kg) - e.g., Earth
M2 = 7.348e23  # Mass of body 2 (kg) - e.g., Moon
dt = 10000  # Time step (s)
steps = 1000  # Number of simulation steps

# Initial positions (m)
r1 = np.array([0, 0, 0], dtype=float)  # Position of body 1
r2 = np.array([384.4e6, 0, 0], dtype=float)  # Position of body 2 (e.g., ~distance from Earth to Moon)

# Initial velocities (m/s)
v1 = np.array([0, 0, 15], dtype=float)  # Initial velocity of body 1
v2 = np.array([0, 1022, 0], dtype=float)  # Initial velocity of body 2 (Moon's orbital speed)

# Arrays to store positions for plotting
r1_list = []
r2_list = []

# Function to calculate the gravitational force
def gravitational_force(r1, r2):
    r = r2 - r1
    dist = np.linalg.norm(r)
    force = G * M1 * M2 / dist**2
    direction = r / dist
    return force * direction

# Simulation loop
for _ in range(steps):
    # Store positions
    r1_list.append(r1.copy())
    r2_list.append(r2.copy())

    # Compute forces
    F12 = gravitational_force(r1, r2)
    F21 = -F12  # Action-reaction pair

    # Update velocities
    v1 += F12 / M1 * dt
    v2 += F21 / M2 * dt

    # Update positions
    r1 += v1 * dt
    r2 += v2 * dt

# Convert lists to arrays for plotting
r1_array = np.array(r1_list)
r2_array = np.array(r2_list)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(r1_array[:, 0], r1_array[:, 1], r1_array[:, 2], label='Body 1', color='blue')
ax.plot(r2_array[:, 0], r2_array[:, 1], r2_array[:, 2], label='Body 2', color='red')

# Labels and legend
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.legend()
ax.set_title('Two-Body Orbit Simulation in 3D')

plt.show()

