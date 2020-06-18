# wah-wah real time
import numpy as np
import pyaudio
import time

RATE = 44100

# BP  filter with narrow pass band,
# fc oscillates up and down the spectrum
# difference ecuation taken from DAFX

# mim and max centre cutoff frequency of variable bandpass filter
cut_min = 500
cut_max = 3000
# wah frecquency
fw = 2000
# change in centre frequency per sample
delta = fw/RATE

# crear una onda triangular con los valores de frecuencias
long = 1024*107

fc = []
while (len(fc)< (long)):
    fc = np.append(fc, np.arange(cut_min, cut_max, delta))
    fc = np.append(fc, np.arange(cut_max, cut_min, -delta))
# quitamos lo que sobra
fc = fc[:long] # 109568 
# fc es el LFO
# size of band pass
Q1 =0.1#0.5# 2# 1# 0.1 #2*0.05
# must be recalculate each time fc changes
F1 = np.zeros(long)
for i in range(long):
    F1[i] = 2*np.sin((np.pi*fc[i]/RATE))
      
yh = np.zeros(1024)
yb = np.zeros(1024)
yl = np.zeros(1024)
ind = 0 # llegará hasta 109568 long

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    # hacemos el computo
    global ind, yh,yb,yl
    
    # para quitarnos referencias negativas
    yh[0] = data[0]
    yb[0] = F1[ind] * yh[0]
    yl[0] = F1[ind] * yb[0]
        
    for n in range(1,1024):
        yh[n] = data[n] - yl[n-1] - Q1*yb[n-1]
        yb[n] = F1[ind+1] * yh[n] + yb[n-1]
        yl[n] = F1[ind+1] * yb[n] + yl[n-1]
        
        ind += 1
        if ind >=109567:# 109568 -1
            #print('ind ', ind)
            ind = 0
    
    sample = yb.astype(np.int16).tostring()
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
