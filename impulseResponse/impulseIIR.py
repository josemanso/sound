#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:35:53 2020

@author: josemo
"""

# impulse response IIR

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response a = 0.8, delay = 20
I = np.zeros(120)
I[0] = 1
bi = np.zeros(20)
bi[0] = 1
ai = np.zeros(20)
ai[0] = 1
ai[-1] = -0.8
impulse_response = lfilter(bi, ai, I)
#plt.figure(2)
plt.plot(impulse_response)
plt.title('Respuesta Impulso IIR')
plt.xlabel('b = 1, a=[1, 0,...,-0.8]')
plt.show()