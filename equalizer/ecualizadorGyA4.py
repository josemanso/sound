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
G = -5
G1 = 5
fcl = 200
fch = 3000
Q = 0.7
#tipo = 'Base_Shelf'  'Treble_Shelf'
fs = 44100

bb, ab = shelving(G, fcl, fs, Q, tipo = 'Base_Shelf')
bh, ah = shelving(G1, fch, fs, Q, tipo = 'Treble_Shelf')

# en paralelo
graves = lfilter(bb,ab, data)
agudos = lfilter(bh,ah, data)
y = graves+agudos
y[y>32768] = 32767
y[y<-32768] = -32767

y = y/2



# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/ecualiGravesAgudos.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
# write wav file

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
time = np.arange(len(data))/fs
plt.plot(time, data,'g--',time, y, 'r--')#,time, data,'g--')
plt.title('Ecualizador grave y agudos')
plt.xlabel('Original green, ecualizada red')
plt.show()
