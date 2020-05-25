#fftline FFT y magnitud
import matplotlib
matplotlib.use('TkAgg')
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from tkinter import TclError

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


# variables ploting
x_line = np.linspace(0, RATE, CHUNK)

fig, (ax, ax2) = plt.subplots(2,figsize=(12,6))

# create a line object with random data
line, = ax.semilogx(x_line, np.random.randn(CHUNK))

# basic formatting fpr axes
ax.set_title('FFT_AUDIO_FORMAT')

ax.set_ylabel('magnitud')

ax.set_ylim(0,100)
ax.set_xlim(20,RATE/2)

line2, = ax2.semilogx(x_line, np.random.randn(CHUNK))
ax2.set_xlabel('frequecy , Hz')
ax2.set_ylabel('magnitud dB')

ax2.set_ylim(-120,0)
ax2.set_xlim(20,RATE/2)
print('stream started')


while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, np.int16)
    #x_line = np.linspace(0, RATE, CHUNK)
    y_fft = np.abs(fft(data))
    mag = -(20*np.log10(y_fft))
    line.set_ydata((y_fft[0:CHUNK])/2**15) #*2/(256*CHUNK))
    
    line2.set_data(x_line, mag)
    
    #update
    try:
        #plt.draw()
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)
    except TclError:
        print('stream stopped')
        break
    
plt.show()
       