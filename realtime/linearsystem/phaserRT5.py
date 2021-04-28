# phaser real time, state variable filter
import numpy as np
import pyaudio
import time
from scipy.signal import sawtooth
import matplotlib.pyplot as plt

RATE = 44100
fs = RATE
"""
long = 1024*7
index = np.arange(long)/(RATE)
flfo = 15
#phaseModulator = 0.8+sawtooth(2*np.pi*flfo*index)
phaseModulator = 0.8+np.sin(2*np.pi*flfo*index)
plt.plot (phaseModulator)
plt.show()
f1 = 300 # frecuencias de corte
f2 = 800
f3 = 1000
f4 = 4000
r1 = 0.9
r2 = 0.98
r3 = 0.8
r4 = 0.9
AP1a2 = r1**2
AP2a2 = r2**2
AP3a2 = r3**2
AP4a2 = r4**2
g = 0.9
y1 = np.zeros(long)
y2 = np.zeros(long)
y3 = np.zeros(long)
y = np.zeros(long)
def phaser(x):
    for i in range(long):
        theta1 = (1/fs)*f1*(1+phaseModulator[i])
        theta2 = (1/fs)*f2*(1+phaseModulator[i])
        theta3 = (1/fs)*f3*(1+phaseModulator[i])
        theta4 = (1/fs)*f4*(1+phaseModulator[i])
    
        AP1a1 = -2*r1*np.cos(theta1)
        AP2a1 = -2*r2*np.cos(theta2)
        AP3a1 = -2*r3*np.cos(theta3)
        AP4a1 = -2*r4*np.cos(theta4)
    
        # Applies each filter using the difference equations
        y1[i] = (AP1a2*x[i]+AP1a1*x[i-1]+x[i-2]
                 -AP1a1*y1[i-1] - AP1a2*y1[i-2])
        y2[i] = (AP2a2*y1[i]+AP2a1*y1[i-1]+y1[i-2]
                 -AP2a1*y2[i-1] - AP2a2*y2[i-2])
        y3[i] = (AP3a2*y2[i]+AP3a1*y2[i-1]+y2[i-2]
                 -AP3a1*y3[i-1] - AP3a2*y3[i-2])
        y[i] = (AP4a2*y3[i]+AP4a1*y3[i-1]+y3[i-2]
                -AP4a1*y[i-1] - AP4a2*y[i-2])
    out = y + g*x
    return out
"""
# mim and max centre cutoff frequency of variable bandpass filter
cut_min = 500
cut_max = 3000
# phaser frecquency
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
plt.plot (fc)
plt.show()
# Chamberlin
#Input/Output
   # I - input sample
   # L - lowpass output sample
   # B - bandpass output sample
   # H - highpass output sample
   # N - notch output sample
   # F1 - Frequency control parameter
   # Q1 - Q control parameter
   # D1 - delay associated with bandpass output
   # D2 - delay associated with low-pass output
   
#L=D2+F1*D1
#H=I-L-Q1*D1
#B=F1*H+D1
#N=H+L
   
Q1 =0.1#0.5# 2# 1# 0.1 #2*0.05
# must be recalculate each time fc changes
F1 = np.zeros(long)
for i in range(long):
    F1[i] = 2*np.sin((np.pi*fc[i]/RATE))
      
yh = np.zeros(1024)
yb = np.zeros(1024)
yl = np.zeros(1024)
yn = np.zeros(1024)
ind = 0 # llegará hasta 109568 long
#yx = []
#yout = np.zeros(long)
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    # hacemos el computo
    
    global ind, yh, yl, yn
    
    # para quitarnos referencias negativas
    yh[0] = data[0]
    yb[0] = F1[ind] * yh[0]
    yl[0] = F1[ind] * yb[0]
    yn[0] = yh[0] + yl[0]
    
    for n in range(1,1024):
        yh[n] = data[n] - yl[n-1] - Q1*yb[n-1]
        yb[n] = F1[ind+1] * yh[n] + yb[n-1]
        yl[n] = F1[ind+1] * yb[n] + yl[n-1]
        yn[n] = yh[n] + yl[n]
        
        ind += 1
        if ind >=109567:# 109568 -1
            #print('ind ', ind)
            ind = 0
        
    #yx = np.append(yx, data)
    #if len(yx) == long:
        #yout = phaser(yx)
        #yx = []
    #sample = yout[:1024]
    #yout = yout[1024:]
    
    #y = phaser(data)
    #sample = sample.astype(np.int16).tostring()
    sample = yn.astype(np.int16).tostring()
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
