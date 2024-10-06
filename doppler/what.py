from matplotlib import pyplot as plt
import numpy as np


c = 299_792_458
def doppler(v):
    ratio = v/c
    return ((1+ratio)/(1-ratio))**0.5

def b(w):
    return 1/w

fig, ax = plt.subplots(1, 2)
ts = np.linspace(0, 64*np.pi, 5000)
ws = [70*doppler(0.5*c*np.cos(t)) for t in ts]
print(min(ws), max(ws))
ys = [np.sin(b(ws[i])*t) for (i, t) in enumerate(ts)]
ax[0].scatter(ts, ys)
ax[1].scatter(ts, ws)

#reflected_ws = [700*doppler(0.5*c*np.cos(t)) for t in ts[::-1]]
#new_ys = [np.sin(b(reflected_ws[i])*t) for (i, t) in enumerate(ts[::-1])]
#plt.scatter(ts, new_ys)
plt.show()