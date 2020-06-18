#overdrive simétrico
import numpy as np
import pyaudio
import time


def simetria(x):
   # th=1/3; threshold for symmetrical soft clipping% by Schetzen Formula
    y = np.zeros(len(x))
    for i in range(len(x)):
        if 0 <=  abs(x[i]) and abs(x[i]) <= 1/3:
            y[i] = 2*x[i]
        elif 1/3<= abs(x[i]) and abs(x[i]) <=2/3:
            y[i] = x[i]/abs(x[i])*(3-(2-3*abs(x[i]))**2)/3
        elif 2/3 <= abs(x[i]) <= 1:
            y[i] = x[i]/abs(x[i])*1#x[i] #1
    
    return y

RATE = 44100

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    data1 = data.copy()
    # hacemos el computo
    data1 = data1/ 32768 # valores entre 1 y -1
    #data1 /= 32768
    y = simetria(data1)
    y *= 32768
    
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


        