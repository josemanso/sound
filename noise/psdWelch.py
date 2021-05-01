#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:45:05 2021

@author: josemo
"""


import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq
from scipy.signal import welch

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "grabacion.wav"
        
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

time = np.arange(len(data))/fs

#freqs, times, spectrogram = signal.spectrogram(data)
freqs, psd = welch(data, fs)

plt.figure()
plt.semilogx(freqs, psd)
plt.title('PSD ')
plt.xlabel('Frecuencias')
plt.ylabel('Power')

