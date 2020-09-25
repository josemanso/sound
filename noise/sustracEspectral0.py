#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:51:55 2020

@author: josemo
"""

#sustracción espectral
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft, fftfreq
from scipy.signal import windows


#The noisy signal y(m) is a sum of the desired signal
# x(m) and the noise n(m);  y(m) = x(m) + n(m)
# In the frequency domain, this may be denoted as:
# Y(jω) = X(jω) + N(jω)  =>  X(jω) = Y(jω) - N(jω)


def drawFFT(fs, wav_data, no_sample_points):
    N = no_sample_points
    # sample spacing
    T = 1.0/fs
    #x = np.linspace(0,N*T, N)
    x = np.arange(N)/fs
    y = wav_data
    #plt.plot(x,y)
    yf = fft(y)
    xf = np.linspace(0.0,1.0/(2.0*T), int(N/2))
    plt.plot(xf, int(2.0/N)*np.abs(yf[:N//2]))
    #plt.plot(xf[:N//2], np.abs(yf[:N//2]))
    freqs = fftfreq(N, 1/fs)
    plt.plot(freqs[:int(freqs.size/2)],np.abs(yf[:int(freqs.size/2)]))
    #plt.plot(abs(yf))
    #plt.show()


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

#drawFFT(fs, data, len(data))
# tenemos al inicio unos 1,5 seg de ruido
noisy= data[:fs] # un segundo
hopsize = min(len(noisy), len(data))
# reshaping the file so that it can be windowed
noise_data = noisy.reshape(1, hopsize)

# applyin Hamming window method
window = windows.hann(hopsize)

noise_data = noise_data*window


# Taking FFT of the windowes noisy data
noise_ffts = fft(noise_data, axis=1)
# Since each funcyion is in complex form, we conver it
# into power fprm (r, theta) and use only r
noise_ffts_abs = np.abs(noise_ffts)
noise_power = noise_ffts_abs**2
print('noise pow ', noise_power.shape)
print(noise_power)
# this means is the noise estimate that will get subtracted
means_power = np.mean(noise_power, axis=0)
print('mens ', means_power.shape, ' valor ', means_power)

# Taking FFT of the signal from wich the noise is to be removed
# constantes para la resta
alpha = 5.0
beta = 0.0005
y =np.zeros(hopsize)

for i in range(0,len(data), hopsize): # min max, step
    # 1 sg; fs tramas
    if i + hopsize >len(data):
        print('i ', i)
        # añadir ceros
        resto = len(data)%hopsize # esto es lo que queda
        falta = hopsize - resto
        print('resto ' , resto)
        print('falta', falta)
        ceros = np.zeros(falta)
        wav_data = data[i:len(data)]
        #wav_data = np.pad(wav_data, (0.0,ceros), 'constant') 
        wav_data = np.insert(wav_data, 1, ceros)
    else:
        wav_data = data[i:i+hopsize]
    print('len wav ', len(wav_data))
    wav_data = wav_data * window
    #wav_data = wav_data.reshape(1,hopsize)
    fft_data = fft(wav_data)#, axis = 1)
    fft_abs = abs(fft_data)
    fft_pow = fft_abs**2
    print('fft_pow ', fft_pow.shape, ' valor ', fft_pow)
    print('fft_data ', fft_data.shape)
    #print(fft_data)
    theta = np.angle(fft_data)
    # creamos un array de lond fft_data
    r = np.zeros(len(fft_data))
    # subtracts power of 'noise data' from fft of original data
    for j in range(len(fft_data)):
        #print('fft_abs de i ', fft_pow[j])
        r[j] = (fft_pow[j] -(alpha * means_power[j]))
        if r[j] <0:
            r[j]= beta* means_power[j]
        r[j] = np.sqrt(r[j])
        
    # converts the complex number of recreated data (r, theta) to x,+ ij form
    reconstructed = (r*np.cos(theta)+r*np.sin(theta)*1j)
    # inverse fft
    reconstructed_sig = ifft(reconstructed)
    
    # extracting original data from the windowed data
    reconstructed_sig /=window
    # taking the real dataof the data that was represented in complex form
    reconstructed_sig = np.real(reconstructed_sig)
    
    y = y + reconstructed_sig
    
# quitamos el primer tramo de ceros  y el resto
print('lon y ', len(y))
y = y[hopsize:]
print('lon y ', len(y)) 
    
     
#data = data*window

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
fig, ax =plt.subplots()
time = np.arange(len(data))/fs
#plt.plot(time, data,'g--',time, y, 'r--')#,time, data,'g--')
#plt.plot(time,data)
ax.plot(time,data)
ax.plot(y)
#plt
ax.plot(data, y)
plt.title('spectral substraction ')
plt.xlabel('Original green, ecualizada red')
plt.show()
