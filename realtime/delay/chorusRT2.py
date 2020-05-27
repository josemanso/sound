# chorus RT
import numpy as np
import pyaudio
import time
import queue as queue

CHUNK = 1024*2 # pyaudi por defecto nos toma 1024 frames
 # por interacción, haremos la computación con dos chunk
# chorus parameters
index = np.arange(CHUNK)
rate1 = 7
rate2 = 10
rate3 = 12
A = 5 # amplitud
lfo1 = A*np.sin(2*np.pi*index*(rate1/CHUNK))
lfo2 = A*np.sin(2*np.pi*index*(rate2/CHUNK))
lfo3 = A*np.sin(2*np.pi*index*(rate3/CHUNK))
# ganancias 1
g = 0.20 

#RATE = 44100
RATE = 16000

delay = int(0.040*RATE) # frames 1764 max= 1764 + 5
# tomaremos dos chunk
q = queue.Queue(2) # dos chunks

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)# ndarray
    q.put(data)
    if q.full():
        # cogemos la última FIFO
        last_data = q.get()
        # hacemos el computo
        for i in range(len(data)):
            data = data.copy()
            M1 = delay + int(lfo1[i])
            M2 = delay + int(lfo2[i])
            M3 = delay + int(lfo3[i])
            if i-M1 < 0:
                dato1 = last_data[1024 +i-M1]
            else:
                dato1 = data[i-M1]
            if i-M2 < 0:
                dato2 = last_data[1024 +i-M1]
            else:
                dato2 = data[i-M1]
            data[i] = g*data[i]+ g*dato1+ g*dato2
    # else
    sample = data.astype(np.int16).tostring()
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


        
    