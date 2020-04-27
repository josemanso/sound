#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:25:19 2020

@author: josemo
"""

# filtro peak

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import freqz#, unit_impulse
import matplotlib.pyplot as plt

# peak filter for EQ
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


fs = 44100
Q = 0.7
fc = fc1 = fc2 = fc3 = fc4= 1000
G = 1
b,a = peakfilter(G,500,fs,Q)
w, h = freqz(b, a, fs)
freq = w*fs/(2*np.pi)
print('freq ', freq.shape)
b1,a1 = peakfilter(G,1000,fs,Q)
w1, h1 = freqz(b1, a1, fs)
freq1 = w1*fs/(2*np.pi)
print('h ', h.shape)
b2,a2 = peakfilter(G,2000,fs,Q)
w2, h2 = freqz(b2, a2, fs)
freq2 = w2*fs/(2*np.pi)
b3,a3 = peakfilter(G,4000,fs,Q)
w3, h3 = freqz(b2, a2, fs)
freq3 = w3*fs/(2*np.pi)
f = np.arange(20000)
b4,a4 = peakfilter(G,8000,fs,Q)
w4, h4 = freqz(b4, a4, fs)
freq4 = w4*fs/(2*np.pi)
# plot
fig, ax =plt.subplots()
#ax.plot(freq, 20*np.log10(abs(h)), 'g--', label='1000')
ax.plot(freq, abs(h), 'r--', label='500')
ax.plot(freq1, abs(h1), 'k--', label='1000')
ax.plot(freq2, abs(h2), 'b--', label='2000')
ax.plot(freq3, abs(h3), 'y--', label='4000')
ax.plot(freq4, abs(h4), 'g--', label='8000')


plt.title('Peak filter')
plt.yscale("log")
plt.xscale("log")
plt.legend()
plt.grid()
plt.show()