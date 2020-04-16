import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, iirnotch, freqz
import matplotlib.pyplot as plt

f1 = 300 # frecuencias de corte
fs = 44000

r1 = 0.98

Q = 30
b1, b2 = iirnotch(f1/(fs/2), Q)
print('b1 ', b1, 'b2 ', b2)
a1 = -2*r1*np.cos(f1/fs)
a2 = r1**2
print('a1', a1, 'a2 ', a2)

b = np.zeros(3)
b[0] = a2
b[1] = a1
b[2] = 1
a = np.zeros(3)
a[0] = 1
a[1] = a1
a[2] = a2


w, h = freqz(b1,b2)
freq = w*fs/(2*np.pi)
w1, h1 = freqz(b,a)

#plot
fig, ax = plt.subplots(2, 1, figsize=(8, 6))

ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')
ax[0].set_xlabel('iirnotch')
ax[1].plot(freq, 20*np.log10(abs(h1)), color='blue')
ax[1].set_xlabel('allpas iirnotch')

#plt.grid()
plt.show()
