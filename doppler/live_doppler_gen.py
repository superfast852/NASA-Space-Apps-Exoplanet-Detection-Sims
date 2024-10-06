from matplotlib import pyplot as plt
import numpy as np


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


def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).
    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    #R *= 255
    #G *= 255
    #B *= 255
    #return (int(R), int(G), int(B))
    return R, G, B, 1


def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def wavelength(x):
    return 404*np.cos(x) + 808


window = AnimatedWindow()
window.ax.set_facecolor("xkcd:salmon")
shift = np.pi/25
compound_shift = 0
pre_mapped = lambda x: map_range(np.clip(x, 400, 1000), 400, 1200, 380, 750)
di = np.pi / 5000
ts = np.arange(0, 2*np.pi+di, di)
while True:
    ys = []
    colors = []
    window.clear()
    acc = 0
    ts += shift
    ws = wavelength(ts)
    for w in ws:
        ys.append(np.sin(acc+compound_shift))
        acc += w/80000
        colors.append(wavelength_to_rgb(pre_mapped(w)))
    compound_shift += shift
    window.ax.scatter(ts, ys, c=np.clip(colors, 0, 1), s=1)
    window.ax.patch.set_alpha(0)
    window.refresh()


plt.show()
