#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:30:26 2020

@author: josemo
"""

# overdrive simétrico, soft clicking
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def simetria(x):
   # th=1/3; threshold for symmetrical soft clipping% by Schetzen Formula
    y = np.zeros(len(x))
    for i in range(len(x)):
        if 0 <=  abs(x[i]) and abs(x[i]) <= 1/3:
            y[i] = 2*x[i]
        elif 1/3<= abs(x[i]) and abs(x[i]) <=2/3:
            y[i] = x[i]/abs(x[i])*(3-(2-3*abs(x[i]))**2)/3
        elif 2/3 <= abs(x[i]) <= 1:
            y[i] = x[i]/abs(x[i])*1#x[i] #1
    
    return y
        

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "guitar.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
        
    
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/josemo/python/wavfiles/"+file_input):
    filename ="/home/josemo/python/wavfiles/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()
    
#
# read wave file
fs, data = wavfile.read(filename)
# nosotros tenemos valores de int16 osea 2¹⁶  / 2(positivos negativos)
# es decir 65536 / 2 = 32768
#data = data/32768
norm = 32768
data = data/norm
# Overdrive simulation
N = len(data)
y = np.zeros(N) # preallocate

y = simetria(data)

# write output file
y = y * norm
data = data *norm

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/overdrive.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
# write wav file
#wavfile.write('/home/josemo/python/wavfiles/reverb1.wav', fs, y.astype(np.int16))

# onda sinuidal
fss = 100
t = np.arange(fss)
p = np.sin(2*np.pi*2*t/fss)
#p = np.sin(t)
z = simetria(p)

#plot
time = np.arange(len(data))/fs
plt.figure(1)
plt.plot(time, data,'g--', time, y, 'r--')
plt.title("Overdrive")
plt.xlabel('Original green, tremolo red')
#plt.figure(2)
f, ax = plt.subplots()
ax.plot(t,p, 'g', label='Original')
ax.plot(t,z,'r--',label='overdrive')
plt.legend()
plt.show()