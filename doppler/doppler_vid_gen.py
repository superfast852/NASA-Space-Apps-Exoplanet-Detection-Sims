from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation as ani


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


shift = 0
pre_mapped = lambda x: map_range(np.clip(x, 430, 1100), 400, 1200, 380, 750)
di = np.pi / 5000
ts = np.arange(0, 2 * np.pi + di, di)
def update(interval: int):
    global shift, ts
    ys = []
    colors = []
    acc = 0
    ws = wavelength(ts+shift)
    for w in ws:
        ys.append(np.sin(acc+shift))
        acc += w / 80000
        colors.append(wavelength_to_rgb(pre_mapped(w)))
    shift += np.pi/30

    ax.cla()
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude (m)')

    colors = np.clip(colors, 0, 1)
    while True:
        try:
            ax.scatter(ts, ys, c=colors, s=1)
            break
        except ValueError:
            pass

    #shift += np.pi/100
    #return points,


fig, ax = plt.subplots()
fig.patch.set_alpha(0.0)
ax.set_facecolor((1, 1, 1, 0))
frames = 60
anim = ani.FuncAnimation(fig, update, frames)
#anim.save("doppler_test.mp4", writer='ffmpeg', fps=30, extra_args=['-vcodec', 'libx264', "-level", "3.0", "-pix_fmt", "yuv420p"])  # For MP4, white background.
anim.save("doppler_test.mov", codec="png", fps=30, dpi=300, bitrate=-1, savefig_kwargs={"transparent": True, 'facecolor': 'none'}, extra_args=["-level", "3.0", "-pix_fmt", "rgba"])