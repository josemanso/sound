import numpy as np
import pyaudio
import time
#import queue as queue

S = 27 # velocidad de la fuente m/seg
Vsonido = 342.0 # m/seg
g = S/Vsonido
RATE = 44100

L = int(RATE *3)
delay = np.zeros(L)
# hay que hacerlo desde g = 0
for h in range(L//2, 0, -1):
    delay[h-1] = delay[h]+g
for j in range(L//2, L-1):
    delay[j+1] = delay[j]+(g)
    
#print('delay ', delay[0])# 5222.368
#print(' delay ', max(delay))

no_chunks = int(delay[0]/1024)+1 #
print('chu ',no_chunks)
no_frames = int(delay[0])+1

#q = queue.Queue(no_chunks)
A = []
ind = -1
y = np.zeros(1024)
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
   
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #q.put(data)
    global A, ind, y
    A = np.append(A, data)
    # hacemos el computo
    l_a = len(A)-1025
    
    if len(A) >= no_frames:
    
        for i in range(1024):
            ind +=1
            if ind >= L-1:
                ind = 0
            
            rpi = int(delay[ind])
            
            a = delay[ind] - rpi
            y[i] = (a*A[(i+l_a)-rpi+1]
                    +(1-a)*A[i+l_a-rpi])
            
        # ahora, quitar el primero de A,
        A = A[1024:]
        
        # actualizar idice de delay, hecho antes

    data_out = y.astype(np.int16).tostring()
    return(data_out, pyaudio.paContinue)
    #return (sample, pyaudio.paContinue)

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

#stream.stop_stream()
stream.close()

pa.terminate()