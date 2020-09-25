# reverb convolution real time
import os
import numpy as np
import pyaudio
import time
from scipy.io import wavfile
from scipy.fftpack import fft, ifft

RATE = 44100 
fs, RIR = wavfile.read("/home/josemo/python/wavfiles/IR/church.wav")
print('fs ', fs, 'RIR ', RIR.shape)
#fs  44100 RIR  (352193,)
# 8 segundos;  necesitamos 344 chunks, 
def fconv(x,h):
    ly = len(x)+len(h) -1
   
    X = fft(x, ly)
    H = fft(h, ly)
    
    Y = X * H  # convolution
    y = np.real(ifft(Y,ly))
    y=y/max(abs(y))
    return y

cola = np.array([])
samples = np.zeros(1024*344)
def callback(in_data, frame_count, time_info, status):
    data = np.frombuffer(in_data, np.int16)
    global cola, samples
    cola = np.append(cola, data)
    if (len(cola) == 344*1204):
        # convolución
        samples = fconv(cola, RIR)
        cola = ([])
    # ahora hay que ir dando datos de 1024 en 1024
    else:
        out = samples[0:1024]
        samples = samples[1024:]
    out = np.array(data, dtype='int16')
    return (out, pyaudio.paContinue)

p = pyaudio.PyAudio()
## open stream
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
        time.sleep(10)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    

stream.stop_stream()
stream.close()

p.terminate()
