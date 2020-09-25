# flanger oflanging, en tiempo real
import numpy as np
import pyaudio
import time
import queue as queue

# parámetros efecto flanger
max_time_delay = 133 # 3 ms
fo = 1 # frecuencia lfo
gff = 0.7 # ganancia a la salida
gfb = 0.5 # ganancia en la realimentación delay, ffedback

# tiempo real
RATE = 44100
CHUNK = 1024

index = np.arange(0, CHUNK, 1)
sin_ref = abs(np.sin(2*np.pi*index*fo/128))

q = queue.Queue(2) #para guardar el anterior, in_data y el actual
#p = queue.Queue(1) #para guardar el computo anterior 
#aux = np.zeros(1024)
y = np.zeros(1024)
#p.put(y)
anterior = np.zeros(1024)

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #array_data = np.append(q.get(), data)
    q.put(data)
    global y, anterior
    
    if q.full():
        # cogemos la última FIFO
        last_data = q.get()
        # hacemos el computo
        for i in range(1024):
            M = int(max_time_delay* sin_ref[i])
            if i-M < 0:
                dato1 = last_data[1024+i-M]# datos del anterior
                comp = anterior[1024+i-M] # computo anterior
            else:
                dato1 = data[i-M]
                comp = y[i-M]
            # y[i] = gfb*y[i-delay] + data[i] + (gff - gfb)*data[i-delay]    
            y[i] = gfb*comp +data[i]+(gff-gfb)*dato1
    y = y/4
    anterior = y    
        
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
