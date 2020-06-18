#ecualizador parámetrico tiempo real
import numpy as np
import pyaudio
import time
from scipy.signal import lfilter

from peakfunction1 import peakfilter
from shelvingFunction import shelving

RATE = 44100
Q = 0.7
def equalizer(Q, fs, data):
    # llamada a la función shelving
    bb, ab = shelving(-3, 100, fs, Q, tipo = 'Base_Shelf')
    bh, ah = shelving(-1, 8000, fs, Q, tipo = 'Treble_Shelf')

    # llamada a la función peak
    b,a = peakfilter(-1, 180,fs,Q)
    b1,a1 = peakfilter(1, 540,fs,Q)
    b2,a2 = peakfilter(2, 1620,fs,Q)
    b3,a3 = peakfilter(3, 4860,fs,Q)

    # filtramos la señal
    #filtro shelving graves
    sl = lfilter(bb, ab, data)
    #filtro peak demenor frecuencia central, o de corte, a mayor
    pa1 = lfilter(a,b,sl)
    #segundo peak
    pa2 = lfilter(b1,a1, pa1)
    # 3º
    pa3 = lfilter(b2,a2, pa2)
    # 4º
    pa4 = lfilter(b3,a3, pa3)
    # y el shelving graves
    y = lfilter(bh,ah, pa4)
    
    y[y>32768] = 32767
    y[y<-32768] = -32767
    
    return y

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #data1 = data.copy()
    # hacemos el computo
    #data1 = data1/ 32768 # valores entre 1 y -1
    #data1 /= 32768
    y = equalizer(Q, RATE, data)
    #y *= 32768
    
    sample = y.astype(np.int16).tostring()
    #return (in_data, pyaudio.paContinue)
    return (sample, pyaudio.paContinue)
# open stream
stream = pa.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
        stream_callback = callback)
stream.start_stream()

while stream.is_active():
    print("Stream is active")
    time.sleep(10)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()


