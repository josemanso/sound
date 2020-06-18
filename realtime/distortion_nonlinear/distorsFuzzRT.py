# distorsión fuzz
import numpy as np
import pyaudio
import time


norm = 32768  # de int16 a valores entre -1 y 1
g = 2 # ganancia gain
def distorfuzz(x, g):         
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))
    
    return y

RATE = 44100

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    data1 = data.copy()
    # hacemos el computo
    data1 = data1/ norm # valores entre 1 y -1
    #data1 /= 32768
    y = distorfuzz(data1, g)
    y *= norm
    
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
