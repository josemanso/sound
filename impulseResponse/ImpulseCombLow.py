#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 18:27:49 2020

@author: josemo
"""

# impulse response comb filter
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response g  = 0.7, delay = 20

I = np.zeros(120)
I[0] = 1
d = 20
g = 0.7 # feedback and feedforwardd
g1 = 0.3
b= np.zeros(d+1)
#b[0] = g
b[-1] = 1

a = np.zeros(d)
a[0] = 1
a[-1] = -g
np.append(a,-g*(1-g1))

impulse_response = lfilter(b, a, I)

y = np.zeros(120)
for i in range(120):
    y[i] = g1*I[i] + g *y[i-d]

plt.figure(1)
plt.plot(impulse_response)
plt.title('Respuesta Impulso comb lowpas filter')
plt.xlabel('delay 10, ganancias 0.5 feedback y 0.3 low pass')
plt.figure(2)
plt.plot(y)
plt.show()