from __future__ import annotations
from typing import *
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3D

class AnimatedWindow:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax = self.fig.gca()
        self.figid = id(self.fig)

    def scatter(self, points):
        self.ax.scatter(*zip(points))

    def refresh(self):
        if id(plt.gcf()) != self.figid:
            raise ValueError("Window does not exist.")

        plt.draw()
        plt.pause(0.0001)

    def clear(self):
        self.ax.cla()


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
    def __init__(self, ax_lim = (-5e8, 5e8)):
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

        #plt.draw()
        plt.pause(0.0001)

    def clear(self):
        self.ax.cla()


def main_3d():
    # Set up the plot
    system = OscilatingSystem(5.972e24, 7.348e23, 384.4e6, [200, 0, 0], [0, 922, 0])
    dt = 10000
    steps = 10000
    ctr = 0
    pt_count = 20

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    pa, pb = system.get_a_pos(), system.get_b_pos()
    # Plot initial positions
    body1_plot, = ax.plot([pa[0]], [pa[1]], [pa[2]], 'bo', label='Body 1')
    body2_plot, = ax.plot([pb[0]], [pb[1]], [pb[2]], 'ro', label='Body 2')
    # Set plot limits and labels
    ax.set_xlim([-5e8, 5e8])
    ax.set_ylim([-5e8, 5e8])
    ax.set_zlim([-5e8, 5e8])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    for _ in range(steps):
        # Compute forces
        system.update(dt)
        pa, pb = system.get_a_pos(), system.get_b_pos()

        # Update the plot data
        body1_plot.set_data([pa[0]], [pa[1]])
        body1_plot.set_3d_properties([pa[2]])
        body2_plot.set_data([pb[0]], [pb[1]])
        body2_plot.set_3d_properties([pb[2]])
        if ctr % pt_count == 0:
            ax.scatter(pa[0], pa[1], pa[2], 'b+')
            ax.scatter(pb[0], pb[1], pb[2], 'r+')
            ctr = 0
        ctr += 1
        # Redraw the plot with a small pause
        plt.pause(0.00001)


def simple_main_3d():
    w = AnimatedWindow3D()
    system = OscilatingSystem(5.972e24, 7.348e23, 384.4e6, [0, 0, 0], [-500, 1022, 0])
    dt = 8000
    steps = 10000
    ctr = 0
    pt_count = 20

    earth = w.add_replottable_object(system.get_a_pos(), 'bo', label="Earth")
    moon = w.add_replottable_object(system.get_b_pos(), 'ro', label="Moon")

    for _ in range(steps):
        system.update(dt)
        w.replot(earth, system.get_a_pos())
        w.replot(moon, system.get_b_pos())

        if ctr % pt_count == 0:
            pa, pb = system.get_a_pos(), system.get_b_pos()
            w.ax.scatter(pa[0], pa[1], pa[2], 'b+')
            w.ax.scatter(pb[0], pb[1], pb[2], 'r+')
            ctr = 0
        ctr += 1
        w.refresh()
    plt.show()




if __name__  != '__main__':
    w = AnimatedWindow()
    system = OscilatingSystem(5.972e24, 7.348e23, 384.4e6, [150, 0, 400], [0, 1022, 0])

    dt = 5000
    steps = 10000
    for _ in range(steps):
        system.update(dt)
        ap, bp = system.get_a_pos()[:2], system.get_b_pos()[:2]
        w.ax.scatter([ap[0]], [ap[1]], c=(0, 0, 1), marker='+')
        w.ax.scatter([bp[0]], [bp[1]], c=(1, 0, 0), marker='+')
        w.refresh()
else:
    #main_3d()
    simple_main_3d()
