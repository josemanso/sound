import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


fs = 1000.0  # Sample frequency (Hz)
f0 = 300.0  # Frequency to be retained (Hz)
Q = 30.0  # Quality factor

def peakfilter(G, fc, fs, Q):
    K = np.tan(np.pi*fc/fs)
    V = 10**(G/20)
    #b0 = (V + np.sqrt(2*V)*K+(K**2))/(1+np.sqrt(2)*K+K**2)
    b0 = (1 +(V/Q)*K + K**2)/(1 + (K/Q) + K**2)
    b1 = (2*((K**2)-1))/(1 + K/Q + K**2)
    b2 = (1 - (V/Q)*K + K**2)/ (1 + K/Q + K**2)
    a1 = (2*((K**2)-1))/(1 + K/Q + K**2)
    a2 = (1-(K/Q) + (K**2))/(1 + K/Q + K**2)
    A = [1, a1, a2] 
    B = [b0, b1, b2]
    return B,A


# Design peak filter
b, a = peakfilter(1, f0, fs, Q)
#b, a = signal.iirpeak(f0/(fs/2), Q)

# Frequency response
freq, h = signal.freqz(b, a)
# Plot
plt.plot(freq, 20*np.log10(np.maximum(abs(h), 1e-5)), color='blue')
plt.title("Frequency Response")
plt.xlabel('freq. ')
plt.ylabel('Amplitude, dB')
plt.show()