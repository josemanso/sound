# wah-wah en tiempo real
import numpy as np
import pyaudio
import time
#import matplotlib.pyplot as plt
from scipy.signal import iirpeak

RATE = 44100
#time = np.arange(1024 *8)
cut_min = 500    # LFO minval, Hz
cut_max = 3000   # LFO maxval, Hz
fw =  2000       # wah frecuency,
# cetro de la frecuencia
delta = fw/RATE # 0,0453
depth = 2   # factor Q, filter iirpeak

# crear una onda triangular con los valores de frecuencias
long = 1024*107
fc = []
while (len(fc)< (long)):
    fc = np.append(fc, np.arange(cut_min, cut_max, delta))
    fc = np.append(fc, np.arange(cut_max, cut_min, -delta))
# quitamos lo que sobra
fc = fc[:long] # 109568 
# fc es el LFO
# ahora calculamos los parámetros del filtro
bs= np.zeros(long*3)# []
ais = np.zeros(long*3)#np.zeros(3)
for i in range(long):
    b, a = iirpeak(fc[i]/(RATE/2), depth)
    for h in range(3):
        bs[(i*3)+h] = b[h]
        ais[(i*3)+h] = a[h]

print('len lfo ', len(fc))
print('b ', len(bs), ' a', len(ais))
#plt.plot(fc)
#plt.show()
y = np.zeros(1024)

ind = 0 # llegará hasta 328704  = 3 x 109568 long
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    # hacemos el computo
    global ind, y
        
    for n in range(2,1024):
        y[n] = (bs[ind]*data[n] + bs[ind+1]*data[n-1]+
                bs[ind+2]*data[n-2]
                -ais[ind+1]*y[n-1]-ais[ind+2]*y[n-2])
        ind += 3
        if ind >328701:
            #print('ind ', ind)
            ind = 0
        
    gain = 0.8
    y = (1-gain)*data +  gain*y
    
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
