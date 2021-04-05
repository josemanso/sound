
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response a = 0.8, delay = 20
I = np.zeros(120)
y = np.zeros(120)
I[0] = 1
a = 0.9
D = 20
""""
bi = np.zeros(20)
bi[0] = -a
bi[-1] = 1
ai = np.zeros(20)
ai[0] = 1
ai[-1] = a # -0.8
#impulse_response = lfilter(bi, ai, I)
"""
#bi = [0,1]
#ai = [1,0]
bi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.9]
ai = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-0.9]
impulse_response = lfilter(bi, ai, I)
#
for i in range(20,120):
    y[i] = -a*I[i] + I[i-D] + a*y[i-D]
    
#plt.figure(2)
#plt.plot(y)#(impulse_response)
plt.plot(impulse_response)
plt.title('Respuesta Impulso all-pass')
#plt.xlabel('b = [-a,0,..., 1] y a=[1, 0,...,a]')
plt.xlabel('a = 0.9, D = 20')
plt.show()