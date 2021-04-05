# impulse response all-pass

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response a = 0.8, delay = 20
I = np.zeros(1200)
I[0] = 1
a = 0.9
bi = np.zeros(20)
bi[0] = -a
bi[-1] = 1
ai = np.zeros(20)
ai[0] = 1
ai[-1] = -a # -0.8
impulse_response = lfilter(bi, ai, I)
#plt.figure(2)
plt.plot(impulse_response)
plt.title('Respuesta Impulso all-pass')
plt.xlabel('b = [-a,0,..., 1] y a=[1, 0,...,a]')
plt.show()