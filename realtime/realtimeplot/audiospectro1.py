# spectrogram
import matplotlib
matplotlib.use('TkAgg')
import pyaudio
#import time
from matplotlib import pyplot as plt
from matplotlib.mlab import window_hanning,specgram
import numpy as np
#from scipy.signal import spectrogram
from tkinter import TclError

def get_specgram(sound, rate):
    a2d, freq, timed= specgram(sound, window=window_hanning,
                               Fs = rate, NFFT=1024,noverlap=1000)
    return a2d, freq, timed

# open stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

CHUNK = 1024*2 # RATE / number of updates per second

# pyaudio object
p = pyaudio.PyAudio()
# stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer = CHUNK)#,

# variable for plotting
x = np.arange(0, 2*CHUNK, 2)

fig, (ax, ax2) = plt.subplots(2, figsize=(15,8))

# create a line object with random data
line, = ax.plot(x, np.random.randn(CHUNK))
# basic formatting for axes
ax.set_title('AUDIO_FORMAT')
ax.set_xlabel('Samples')
ax.set_ylabel('volume')
ax.set_ylim(-10000,10000)
ax.set_xlim(0,CHUNK)

im = ax2.imshow(np.random.randn(30, 30),aspect='auto',
                interpolation="none",
                    cmap = 'jet')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Frequencies (Hz)')

print('stream started')
while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, np.int16)
    line.set_ydata(data)
    spec2D, freqs, time= get_specgram(data, RATE)
    #im = plt.imshow(arr2D,aspect='auto',extent = extent,interpolation="none",
                    #cmap = 'jet',norm = LogNorm(vmin=.01,vmax=1))
    im.set_data(spec2D)
   
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)
    except TclError:  
        print('stream stopped')
        break
    

plt.show() 