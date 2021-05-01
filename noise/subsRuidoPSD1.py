#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:55:16 2021

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
from scipy.signal import hann

"""
def noise_reduction_fft(data_in):
    N = len(data_in)
    t = np.arange(N)/44100
    fft_data= fft(data_in,N)
    FFT_size = fft_data[range(len(data))//2]
    freqs = fftfreq(data_in.size, time[1]-time[0])
    PSD = PSD = fft_data * np.conj(fft_data) / N
    indices = PSD > 50000  # finf all frequenciies with large power
    filtered = fft_data*indices
    filt = ifft(filtered)
    return filt
"""
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

# ejecutando el algorritmo
#denoise = noise_reduction_fft(data)
N = len(data)
#t = np.arange(N/fs)#/fs

fft_data= fft(data,N)

# abs
fftabs = np.abs(fft_data)
#freqs = fftfreq(len(data), 1/fs)

PSD = PSD = fft_data * np.conj(fft_data) / N

PSD0 = np.where(PSD<5000, 0, PSD) # 

indices = PSD > 50000  # finf all frequenciies with large power
filtered = fft_data*indices
filt = ifft(filtered)

freqs = fftfreq(len(data), 1/fs)

#fft_freqs = np.array(freqs)
#freqs_side = freqs[range(N//2)] # one side frequency range
#fft_freqs_side = np.array(freqs_side)

# salida
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/ruidolessFFT.wav',
                      fs, filt.real.astype(np.int16))                  
                       #fs, y.real.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

# plot 
time = np.arange(len(data))/fs
L = int(N//2)
#freql = time
#plt.plot(time, data)

#fig, ax = plt .subplots(3,1)
#fig, ax = plt .subplots(3)
plt.figure(1)
#ax[0].plot(time. data)
#ax[0].set_xlabel('archivo inicial')
plt.plot(time[:N//2], PSD[:N//2], label = 'Ruidoso')
plt.plot(time[N//2], PSD0[N//2], color ='k', label = 'limpio')
plt.axhline(50000, ls = '--', c='r')
plt.xlim(time[0], time[N//2])
#plt.ylim(0, 32768**2)
plt.ylim(0, 600000)
plt.legend()
plt.xlabel('PSD ')
"""
# fft
#m = len(data)//2
#ax[1].plot()
plt.figure(2)
plt.title('FFT')
plt.xlim( [10, fs/2] )
plt.xscale('log')
plt.grid(True)
plt.xlabel('Frecuencia, Hz')
plt.ylabel('Magnitud')
plt.plot(freqs[:int(freqs.size/2)], fftabs[:int(freqs.size/2)])
#ax[1].set_title('FFT')
#ax[1].set_xlim( [10, fs/2] )
#ax[1].set_xscale('log')
#ax[1].set_grid(True)
#ax[1].set_xlabel('Frecuencia, Hz')
#ax[1].set_ylabel('Magnitud')
#ax[1].plot(freqs[:int(freqs.size/2)], fftabs[:int(freqs.size/2)])

plt.figure(3)
plt.plot(time, filt, 'r--', time, data, 'g--')
plt.plot(time, data, 'g--', time, filt, 'r--')
plt.xlabel('archivo filtrado')
"""
plt.figure(4)
plt.plot(time[:L], PSD[:L], 'g--', time[:L], PSD0[:L], 'r--')
"""
m = int(freqs.size/2) #N//2
plt.plot(freqs[:m], PSD[:m],label = 'Ruido')
plt.plot(freqs[:m], filtered[:m], c ='k', label = 'Limpia')
plt.axhline(500, ls = '--', c ='r')
plt.xlim(freqs[0], freqs[m])
plt.legend(loc=1)
"""
