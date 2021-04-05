import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import freqz, lfilter
import matplotlib.pyplot as plt


warp_factors = np.linspace(-0.99, 0.99, 5)

fig1, ax11 =plt.subplots(figsize =(10,7))
ax11.grid()
plt.title(r'respuesta en frecuencia polo variable $\lambda$')
plt.ylim(-1, 1)
plt.ylabel('amplitud (dB)', color = 'C0')
plt.xlabel(r'frecuencia normalizada (x$\pi$rad/sample)')

for i, wf in enumerate(warp_factors):
    w, h = freqz([-wf, 1.0], [1.0, -wf])
    ax11.plot(w/max(w), 20*np.log10(abs(h)), 'C{0}'.format(i), label = wf)

ax21 = ax11.twinx()
plt.ylabel('fase (radianes)', color ='g')

for i, wf in enumerate(warp_factors):
    w, h = freqz([-wf, 1.0], [1.0, -wf])
    angles = np.unwrap(np.angle(h))
    ax21.plot(w/max(w), angles, 'C{0}'.format(i), label = wf)
ax11.legend(loc= 'upper right')

#x = np.sin
plt.axis('tight')
plt.show()

