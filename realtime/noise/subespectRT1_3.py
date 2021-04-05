#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 10:03:12 2020

@author: josemo
"""

# Susbtracción espectral del ruido
import sys
import os
import numpy as np
import pyaudio
import time
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
from scipy.signal import hann

def noise_mean(data_noise, f_size, n_frames, alpha):
    # data is the complete signal
    # f_size is the size o f frames, nº points, windowing
    # n_frames is the number of noise frames
    # overlap 50%
    
    # samples stores a list of overloappedwindow size
    samples = []
    
    # phases stores a list phases information of every frames
    #phases  =[]
    # nº de ventanas que tendremos
    lps = int(len(data_noise)/f_size) +1
    
    # Hann window
    hn_win = hann(f_size)
    
    for i in range(lps*2):
        
        # estract 50% overlapping frames of f_size of signal
        # and append to samples
        f_loc = int(i*f_size/2)
        samples.append(np.asarray(data_noise[f_loc:f_loc+f_size]))
        
        # Apply Hann window, FFT,
        # save information in list phases
        # estract magnitude
        elem = len(samples) -1
        samples[elem] = samples[elem] * hn_win[:len(samples[elem])]
        samples[elem] = fft(samples[elem])
        #phases.append(np.angle(samples[elem]))
        samples[elem] = abs(samples[elem])
        
        if (len(samples[elem]) < f_size):
            # sino hay tramas suficientes
            break
        
    # assuming first few frames are only noisy frames,
    # Sum all the noisy frames in one frame
    noise = np.asarray(samples[0])
    for i in range(1, n_frames):
        # sumamos arrays,
        # elemento a elemnto y nos quedamos con una
        noise = list(map(lambda x, y : x+y, noise, samples[i]))
        
    # Get an average noise magnitude
    noise = list(map(lambda x: x/n_frames, noise))
    noise = np.mean(noise) # ya tenemos un valor medio
    print('noise ', noise)    
    # multiply bia to noises, factor de aumento del ruido
    #noise *=7
    noise*=alpha
    
    return noise




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
fs, datan = wavfile.read(filename)
print('data ', datan.shape, ' fs ', fs)

RATE = fs
window_size = 400 #512
noise_frames = 100# máximo,como tenemos overlap 50%, 0,6s
alpha = 5
y_noise =noise_mean(datan, window_size, noise_frames, alpha)

# tenemos el ruido de fondo
signal_in =[]
# Hann window
hn_win_n = hann(1024)
f_size_n = 1024
def noiseless(noise_m, data_in):
    # data_in data in
    # noise_m noise mean
    
    y = np.zeros((3072), dtype='complex')
    samples = []
    phases = []
    global signal_in
    signal_in = np.append(signal_in, data_in)
    if len(signal_in) < 3072: # 3 x1024
        #print('signal_in ', signal_in)
        return data_in
    else:
        # numero de ventanas overlap 50%
        # nº de ventanas que tendremos
        #lps = int(len(data)/f_size) +1
        #lps =  4 # 3072/1024 +1  int(len(data)/f_size) +1
        for i in range(5): # 5 para overlap 50% de 3 x 1024 (lps*2):
            # estract 50% overlapping frames of f_size of signal
            # and append to samples
            f_loc = int(i*f_size_n/2)
            samples.append(np.asarray(signal_in[f_loc:f_loc+f_size_n]))
            
            # Apply Hann window, FFT,
            # save information in list phase
            # estract magnitude
            elem = len(samples) -1
            samples[elem] = samples[elem] * hn_win_n[:len(samples[elem])]
            #print ('samples', samples)
            samples[elem] = fft(samples[elem])
            phases.append(np.angle(samples[elem]))
            samples[elem] = abs(samples[elem])
            
        # perform spectra subtraction
        samples = [list(map(lambda x : x - y_noise, h)) for h in samples]
        # perform half wave rectification
        for idx, frm in enumerate(samples):
            samples[idx] = [0 if j < noise_m else j for j in frm]
            
        # Perform IrFFT
        for k in range(len(samples)-1):
            # formula de Euler
            samples[k] =list(map(lambda x, y: x*np.exp(1j*y), samples[k], phases[k]))
            samples[k] = ifft(samples[k])
            # overlap
            ind = int(f_size_n/2)
            # primero
            if k == 0:
                y[:len(samples[k])] = samples[k]
            else:
                for l in range(f_size_n):
                    #print('indices k ', k,'l ',l)
                    y[k*ind+l] = samples[k][l] + y[k*ind+l]
    signal_in = signal_in[1024:] # quitamosel primero
    # devolvemos el 2ª 1024-2048
    return y[1024:2048]
        
    

def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
   
    global signal_in#, signal_out
    #signal_in = np.append(signal_in, data)
    #if len(signal_in) == 3072: #3x 1024 data
    y = noiseless(y_noise, data)
    #y = np.real(y)
    #print('y ',y.dtype)
    y = y.real
    y = y.astype(int)
    #print('y ',y.dtype)
    #y_int = y.astype(int32)
    print('y_i ',y.dtype)
    #print('y ', y)
        # hacemos el computo
        #signal_out = noiseless(signal_in)
        # quitamos el primer chunk
        #signal_in = signal_in[1024:]
    #y = y.astype(np.int16).tostring()
    y = y.astype(np.int32).tobytes()
    #print('y ',y.dtype)
    return (y, pyaudio.paContinue)
    #return (data, pyaudio.paContinu
p = pyaudio.PyAudio()
## open stream using callback
stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
        stream_callback = callback)

stream.start_stream()
try:
    while stream.is_active():
        print("Stream is active")
        time.sleep(12)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    

stream.stop_stream()
stream.close()

p.terminate()
        
