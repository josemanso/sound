#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 09:12:29 2020

@author: josemo
"""

# Fuzz
# distortion based on an exponential function
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
#import math

def distorfuzz(x, g):         
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))
    
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
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()

# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# normalizemos el data, lo hacemos valer entre 1 y -1
# nosotros tenemos valores de int16 osea 2¹⁶  / 2(positivos negativos)
# 65536 / 2 = 32768
norm = 32768

datan = data/norm
print('datann ', datan.shape, ' fs ', fs)
print('nor ', datan)

y = np.zeros(len(datan))
g = 2 # ganancia
y = distorfuzz(datan,g)

# lo ponemos a 16 bits
y = y*32767


# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/distorsionfuzz.wav',
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
z = distorfuzz(p, g)
#plot
time = np.arange(len(data))/fs
plt.figure(2)
#plt.plot(time, data,'g--', time, y, 'r--')
plt.plot(time, y,'r--', time, data, 'g--')
plt.title("Distorsión Fuzz")
plt.xlabel('Original green, distorsión red')

f, ax = plt.subplots()
ax.plot(t,p, 'g', label='Original')
ax.plot(t,z,'r--',label='distor/fuzz')
ax.legend(loc='upper right')
plt.show()