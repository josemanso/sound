#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:02:18 2020

@author: josemo
"""

# respuesta impulso shelving
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt

from shelvingFunction import shelving

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

# filtro Shelving de 2º orden
# set Parameters for Shelving Filter 
G = 5
G1 = -5
fcl = 200
fch = 3000
Q = 0.7
#tipo = 'Base_Shelf'  'Treble_Shelf'
#fs = 44100

if G == 0:
    y_base = data
    bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
    y_treble = lfilter(bt,at,data)
elif G1 ==0:
    bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
    y_base = lfilter(bb,ab,data)
    y_treble = data
else:
    bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
    bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
    y_base = lfilter(bb,ab,data)
    y_treble = lfilter(bt,at,data)
    
y = y_base + y_treble
y = y/2.3

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/ecualiGravesAgudos2.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
# write wav file
#wavfile.write('/home/josemo/python/wavfiles/ring1.wav', fs, y.astype(np.int16))

#fs1, data1 = wavfile.read('/home/josemo/python/wavfiles/ring1.wav')

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
time = np.arange(len(data))/fs
plt.plot(time, y, 'r--',time, data,'g--')
plt.title('Ecualizador grave y agudos')
plt.xlabel('Original green, ring red')
plt.show()
