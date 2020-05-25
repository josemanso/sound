#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:27:11 2020

@author: josemo
"""
import matplotlib
matplotlib.use('TkAgg')
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft 
import time
from tkinter import TclError

CHUNK = 1024 * 4 #4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# pyaudio object
p = pyaudio.PyAudio()
 
stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE, input = True,
        output = True,
        frames_per_buffer = CHUNK)

# variable for plotting
x = np.arange(0, 2*CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

fig, (ax, ax2) = plt.subplots(2, figsize=(15,8))

# create a line object with eandom data
line, = ax.plot(x, np.random.randn(CHUNK))

line_fft, = ax2.semilogx(x_fft, np.random.randn(CHUNK))

# basic formating for axes
ax.set_title('AUDIO_FORMAT')
ax.set_xlabel('Samples')
ax.set_ylabel('volume')

ax.set_ylim(-10000,10000)
ax.set_xlim(0,CHUNK)

#ax2.set_title('AUDIO_FORMAT')
ax2.set_xlabel('frecuencias')
ax2.set_ylabel('magnitud')

ax2.set_ylim(0,5)
ax2.set_xlim(20, RATE / 2)

print('stream started')

# for measuring frame rate
frames_count = 0
start_time = time.time()


while True:
    data = stream.read(CHUNK)
    data_int = np.frombuffer(data, np.int16)
    
    line.set_xdata(np.arange(len(data_int)))
    
    line.set_ydata(data_int)
    
    y_fft = fft(data_int)
    #y_fft = np.abs(fft(data_int))
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK])*2/(256*CHUNK))
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)
        frames_count +=1
    except TclError:
        # calculate average frame rate
        frame_rate = frames_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
    

plt.show() 