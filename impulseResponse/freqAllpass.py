# respuesta en frecuencia allpass
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter, freqz
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
w, h = freqz(impulse_response)
#w, h = freqz(hn)
#plt.figure(2)
fig, ax1 = plt.subplots()
ax1.set_title("Respuesta en frecuencia IIR")
ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Amplitud [dB]', color = 'b')
ax1.set_xlabel('Frequency [rad/sample]')
ax2 = ax1.twinx()
angles = np.unwrap(np.angle(h))
ax2.plot(w, angles, 'g')
ax2.set_ylabel('Angle(radians)', color ='g')
ax2.grid()
ax2.axis('tight')
plt.show()