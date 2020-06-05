# flanger oflanging, en tiempo real
import numpy as np
import pyaudio
import time

max_time_delay = 133 # 3 ms
fo = 1 # frecuencia lfo
gff = 0.7 # ganancia a la salida
gfb = 0.5 # ganancia en la realimentación delay, ffedback

# tiempo real
RATE = 44100
CHUNK = 1024

index = np.arange(0, CHUNK, 1)
sin_ref = abs(np.sin(2*np.pi*index*fo/CHUNK))

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
   
    # hacemos el computo
    y = np.zeros(len(data))
    y[:max_time_delay]= data[:max_time_delay]
    
    for i in range(max_time_delay+1,len(data)):
        delay = max_time_delay * sin_ref[i]
        delay = int(delay)
        
        y[i] = gfb*y[i-delay] + data[i] + (gff - gfb)*data[i-delay]
       
    #sample = y.tostring()
    y = y/3
    sample = y.astype(np.int16).tostring()
    
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
