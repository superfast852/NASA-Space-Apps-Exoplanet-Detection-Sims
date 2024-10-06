import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class OscilatingSystem2D:
    G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)

    def __init__(self, ma, mb, d, a_init_v = (0, 0), b_init_v = (0, 1022)):
        self.ma = ma  # The mass of body A
        self.mb = mb  # The mass of body B
        self.d = d  # The distance between both

        self.ax, self.bx = np.array([0, 0], dtype=float), np.array([d, 0], dtype=float)
        self.av, self.bv = np.array(a_init_v, dtype=float), np.array(b_init_v, dtype=float)
        self.get_a_pos = lambda: self.ax
        self.get_b_pos = lambda: self.bx

    def gravitational_force(self):
        r = self.bx - self.ax
        dist = np.linalg.norm(r)
        force = self.G * self.ma * self.mb / dist ** 2
        direction = r / dist
        return force * direction

    def update(self, dt):
        F_ab = self.gravitational_force()
        F_ba = -F_ab  # act-react

        # Note that F/m = accel
        self.av += F_ab / self.ma * dt
        self.bv += F_ba / self.mb * dt

        self.ax += self.av * dt
        self.bx += self.bv * dt


system = OscilatingSystem2D(6.4524e24, 4.348e23, 84.4e7, [0, 0], [0, 700])
fig, ax = plt.subplots(1, 3, figsize=(12, 6))

reference_comets = [(6e9, -6e9), (-6e9, 6e9), (-4e9, -2e9)]
distances: list = [ax[0].plot([system.ax[0], comet[0]], [system.ax[1], comet[1]+system.ax[1]], 'g-')[0] for comet in reference_comets]
ax[0].set_xlim([-8e9, 8e9])
ax[0].set_ylim([-8e9, 8e9])
ax[1].set_xlabel("Time (s)")
ax[2].set_xlabel("Time (s)")
ax[1].set_ylabel("X Displacement (m)")
ax[2].set_ylabel("Y Displacement (m)")
points = [(system.ax[0], system.ax[1]), (system.bx[0], system.bx[1])] + reference_comets

replots = [ax[0].scatter(*pt) for pt in points]
dt = 86400
t = 0
def update(frame):
    global t
    system.update(dt)
    replots[0].set_offsets(system.ax)
    replots[1].set_offsets(system.bx)
    [distances[i].set_data(*np.array([system.ax, reference_comets[i]]).T) for i in range(len(distances))]

    ax[1].scatter(t, system.ax[0], s=1, c=[(0, 0, 1, 1)])
    ax[2].scatter(t, system.ax[1], s=1, c=[(0, 0, 1, 1)])
    t += dt
    return distances + replots

ani = FuncAnimation(fig, update, frames=300, blit=True)
ani.save("neighbors.mp4", writer='ffmpeg', fps=30, dpi=180, extra_args=['-vcodec', 'libx264', "-level", "3.0", "-pix_fmt", "yuv420p"])  # For MP4, white background.
