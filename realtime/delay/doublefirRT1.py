#  Doubling, double track, en tiempo real
import numpy as np
import pyaudio
import time
from scipy.signal import lfilter
import queue as queue

# parámetros para el efecto doubling
delay = 280 #  5 ms 220 tramas
b = np.zeros(delay)
b[0]= 1 # señal1
b[-1]= 1 # retraso
b /=sum(b)
#print('b ', b)


RATE =44100
q = queue.Queue(1) #para guardar el anterior, in_data
aux = np.zeros(1024)
q.put(aux)

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    array_data = np.append(q.get(), data)
    #print('array ', len(array_data))
    q.put(data)

    # hacemos el computo
    
    data_filt = lfilter(b,1,array_data) #/2
    y = data_filt[1024:]
    
    sample = y.astype(np.int16).tostring()
    
    return (sample, pyaudio.paContinue)
# open stream
stream = pa.open(
        format = pa.get_format_from_width(2), # un byte
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