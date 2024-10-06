from __future__ import annotations
from typing import *
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3D


class OscilatingSystem:
    G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)

    def __init__(self, ma, mb, d, a_init_v = (0, 0, 15), b_init_v = (0, 1022, 0)):
        self.ma = ma  # The mass of body A
        self.mb = mb  # The mass of body B
        self.d = d  # The distance between both

        self.ax, self.bx = np.array([0, 0, 0], dtype=float), np.array([d, 0, 0], dtype=float)
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


class AnimatedWindow3D:
    def __init__(self, ax_lim = (-5e9, 5e9)):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.figid = id(self.fig)

        self.ax.set_xlim(ax_lim)
        self.ax.set_ylim(ax_lim)
        self.ax.set_zlim(ax_lim)
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')

    def add_replottable_object(self, initial_position: np.ndarray | List, *args, **kwargs):
        if len(initial_position) != 3:
            raise ValueError("Initial position must be an iterable of length 3.")
        obj_plt, = self.ax.plot([initial_position[0]], [initial_position[1]], [initial_position[2]], *args, **kwargs)
        return obj_plt

    def replot(self, obj: Line3D, position: np.ndarray | List):
        obj.set_data([position[0]], [position[1]])
        obj.set_3d_properties([position[2]])

    def refresh(self):
        if id(plt.gcf()) != self.figid:
            raise ValueError("Window does not exist.")

        plt.pause(0.0001)

    def clear(self):
        self.ax.cla()


def simple_main_3d():
    # Clear Orbit Values: 5.4524e26, 7.348e23, 384.4e7, 0, [0, 3000, 0]
    w = AnimatedWindow3D()
    system = OscilatingSystem(5.4524e26, 7.348e23, 384.4e7, [0, 0, 500], [0, 3000, 0])
    dt = 43200  # In seconds, orbit of 85 days.
    steps = 10000
    ctr = 0
    pt_count = 10

    earth = w.add_replottable_object(system.get_a_pos(), 'bo', label="Sun")
    moon = w.add_replottable_object(system.get_b_pos(), 'ro', label="Exoplanet")

    for _ in range(steps):
        system.update(dt)
        w.replot(earth, system.get_a_pos())
        w.replot(moon, system.get_b_pos())
        if ctr % pt_count == 0:
            pa, pb = system.get_a_pos(), system.get_b_pos()
            #w.ax.scatter(pa[0], pa[1], pa[2], c="b", marker="o")
            w.ax.scatter(pb[0], pb[1], pb[2], c='r', marker='o')
            ctr = 0
        ctr += 1
        w.refresh()
    plt.show()


if __name__  == '__main__':
    simple_main_3d()
