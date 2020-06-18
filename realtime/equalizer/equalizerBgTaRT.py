#ecualizador graves y agudos tiempo real
import numpy as np
import pyaudio
import time
from scipy.signal import lfilter

from shelvingFunction import shelving

G_base = 5
G_trev = -5
fclow = 200
fchigh = 3000
Q = 0.7

RATE = 44100

def gaincontrol(G, G1, Q, fcl, fch, data):
    if G == 0:
        y_base = data
        bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
        y_treble = lfilter(bt,at,data)
    elif G1 ==0:
        bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
        y_base = lfilter(bb,ab,data)
        y_treble = data
    else:
        bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
        bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
        y_base = lfilter(bb,ab,data)
        y_treble = lfilter(bt,at,data)
    
    y = y_base + y_treble
    y = y/2.3
    return y


pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #data1 = data.copy()
    # hacemos el computo
    #data1 = data1/ 32768 # valores entre 1 y -1
    #data1 /= 32768
    y = gaincontrol(G_base, G_trev, Q, fclow, fchigh, data)
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

