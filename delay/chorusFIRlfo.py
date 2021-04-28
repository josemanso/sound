# chorus
import matplotlib
matplotlib.use('TkAgg')
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       #file_input = "channel_1.wav"
       file_input = "guitar.wav" 
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/josemo/python/wavfiles/"+file_input):
    filename ="/home/josemo/python/wavfiles/"+file_input
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()

# read wave file
fs, data = wavfile.read(filename)
print(' fs', fs,' shapes ', data.shape, ' data ', data)

# tipical delay, entre 10 y 50 ms, LFO entre 5 y 14 Hz
# chorus parameters
index = np.arange(len(data))
rate1 = 7
rate2 = 10
rate3 = 12
A = 5 # amplitud
lfo1 = A*np.sin(2*np.pi*index*(rate1/fs))
lfo2 = A*np.sin(2*np.pi*index*(rate2/fs))
lfo3 = A*np.sin(2*np.pi*index*(rate3/fs))
# ganancias 1
g = 0.20 

delay = int(0.040*fs) # frames

y = np.zeros(len(data))
y[:delay+5] = data[:delay+5]
for i in range (delay +5, len(data)):
    M1 = delay +int(lfo1[i])
    M2 = delay + int(lfo2[i])
    M3 = delay +int(lfo3[i])
    y[i] = g*data[i] + g*data[i-M1]+g*data[i-M2]+g*data[i-M3]
    #y[i] = data[i] + data[i-m1]+data[i-m2]+data[i-m3]

#y = y/4.5

print('y ', y.shape, 'datos ', y)
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/chorus.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)  
#plot
plt.figure(figsize=(8,5))
time = np.arange(len(data))/fs
plt.plot(time, data, 'g--',time, y,'r--')
plt.title('Chorus')
plt.xlabel('Rojo datos chorus, verde, audio original')

plt.show()