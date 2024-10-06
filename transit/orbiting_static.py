import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


# Parameters
sun_radius = 2  # Radius of the sun
exp_radius = 1.25  # Radius of the exoplanet
sun_exp_distance = 5+sun_radius+exp_radius  # Distance between the sun and the exoplanet
orbit_time = 10  # Time it takes for a full orbit
orbit_count = 2
total_time = orbit_time*orbit_count
framerate = 30
framecount = framerate*orbit_time*orbit_count
dt = 1/30


# Calculate exoplanet orbit path
def get_orbit_position(t):
    angle = 2 * np.pi * (t % orbit_time) / orbit_time
    x = sun_exp_distance * np.cos(angle-np.pi/2)
    y = sun_exp_distance * np.sin(angle-np.pi/2)
    return x, y


def calculate_light_intensity(x, y):
    # Calculate the distance between the sun and the exoplanet centers
    if abs(x)>(sun_radius+exp_radius) or y<0:
        # No overlap, full light intensity
        return 1.0
    elif abs(x)<=abs(sun_radius-exp_radius):
        # Full overlap (exoplanet completely covers part of the sun)
        overlap_area = np.pi * min(sun_radius, exp_radius) ** 2
    else:
        # Partial overlap, calculate using circle overlap formula
        dist_centers = abs(x)
        d1 = (sun_radius**2 - exp_radius**2 + dist_centers**2)/(2*dist_centers)
        d2 = dist_centers - d1

        left_side = sun_radius**2*np.arccos(d1/sun_radius) - d1*np.sqrt(sun_radius**2 - d1**2)
        right_side = exp_radius**2*np.arccos(d2/exp_radius) - d2*np.sqrt(exp_radius**2 - d2**2)
        overlap_area = left_side + right_side

    # Calculate intensity as remaining light after overlap
    return 1 - overlap_area / (np.pi * sun_radius ** 2)


# Prepare plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 10))
ax1.set_aspect('equal', 'box')
ax1.set_xlim(-2 * sun_exp_distance, 2 * sun_exp_distance)
ax1.set_ylim(-2 * sun_exp_distance, 2 * sun_exp_distance)
ax2.set_xlim(0, total_time)
ax2.set_ylim(0, 1.1)

# Drawing the sun and initializing the exoplanet
sun_circle = plt.Circle((0, 0), sun_radius, color='yellow', alpha=0.6)
exp_circle = plt.Circle((sun_exp_distance, 0), exp_radius, color='blue', alpha=0.6)
ax1.add_patch(sun_circle)
ax1.add_patch(exp_circle)
intensity_line, = ax2.plot([], [], color='orange')

# Initialize light intensity data list
light_intensities = [calculate_light_intensity(*get_orbit_position(0))]


# Update function for animation
t = 0
true_t = 0
times = [0]
prev_time = time.time()

def frame_gen():
    i = -1
    while true_t<total_time:
        i +=1
        yield i

def update(frame):
    global times, light_intensities, t, prev_time, true_t
    t += dt
    true_t += dt
    # Update exoplanet position
    x, y = get_orbit_position(t)
    exp_circle.set_center((x, y))

    # Update light intensity
    intensity = calculate_light_intensity(x, y)
    light_intensities.append(intensity)

    # Update intensity plot with correct array shapes
    times.append(t)
    intensity_line.set_data(times, light_intensities)

    if (t >= total_time):
        times=[]
        t=0
        light_intensities = []
    #plt.draw()
    #plt.pause(0.00001)
    return intensity_line, light_intensities

#plt.show()
ani = FuncAnimation(fig, update, frames=frame_gen, cache_frame_data=False)
ani.save("transit_sim.mp4", writer='ffmpeg', fps=framerate, extra_args=['-vcodec', 'libx264', "-level", "3.0", "-pix_fmt", "yuv420p"])  # For MP4, white background.
