#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:35:53 2020

@author: josemo
"""

# impulse response FIR, g 0 0.8, delay 10--12

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response a = 0.8, delay = 15
I = np.zeros(120)
I[0] = 1
bi = np.zeros(120)
bi[0] = 1
bi[15] = 1 # 0.8
bi[30] = 1 #0.6
bi[45] = 1 #0.4
bi[60] = 1 #0.2
bi[75] = 1#0.1
bi[90] = 1
bi[105] = 1
#bi[110] = 1
impulse_response = lfilter(bi, 1, I)
#plt.figure(2)
plt.plot(impulse_response)
plt.title('Respuesta Impulso FIR')
plt.xlabel('coeficientes b a 1')
plt.show()