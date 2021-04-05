# repuesta en frecuencia all pass
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import freqz, lfilter
import matplotlib.pyplot as plt

I = np.zeros(120)
y = np.zeros(120)
I[0] = 1
b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.9]
a = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-0.9]
ai = [1,0]
bi = [0,1]
#impulse_response = lfilter(b, a, I)
# mejor con una señal
x = np.sin(np.linspace(-np.pi, np.pi, 20))
y1 = lfilter(b, a, x)
y2 = np.append([0], x[:-1])
samples = np.arange(max(max(len(x), len(y1)), len(y2)))
#w, h = freqz(impulse_response)
sign = 2*np.sin(2* np.pi*45*(np.arange(200)))
#w, h = freqz(b,a,sign)
w, h = freqz(bi,ai)
fig1, ax11 = plt.subplots(figsize = (10, 7))
plt.title ('Respuesta en frecuencia por unidad de retardo')
plt.plot(w/max(w), 20* np.log10(abs(h)), 'b')
plt.ylim(-1,1)
plt.ylabel('Amplitud (dB)', color = 'b')
plt.xlabel(r'frecuencia normalizada (x$\pi$rad/sample)')
ax11.grid()
ax21 = ax11.twinx()
angles = np.unwrap(np.angle(h))
plt.plot(w/max(w), angles, 'g')
plt.ylabel('fase (radianes) ', color = 'g')
plt.axis('tight')
plt.show()
