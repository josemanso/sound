# phaser o phasing
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import iirnotch, sawtooth
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
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
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

time = np.arange(len(data))/fs

flfo = 15

f1 = 300 # frecuencias de corte minima
f2 = 800
f3 = 1000
f4 = 4000

lfo = 2+sawtooth(2*np.pi*flfo*time)
g = 0.7 # gain signal
Q = 2 # factor de calidad

y1 = np.zeros(len(data))
y2 = np.zeros(len(data))
y3 = np.zeros(len(data))
y = np.zeros(len(data))

for i in range(2,len(data)):
    b, a = iirnotch(f1/fs*lfo[i], Q)
    y1[i] = (b[0]*data[i]+b[1]*data[i-1]+b[2]*data[i-2]
             -a[1]*y1[i-1]-a[2]*y1[i-2])
    
for i in range(2,len(data)):
    b, a = iirnotch(f2/fs*lfo[i], Q)
    y2[i] = (b[0]*y1[i]+b[1]*y1[i-1]+b[2]*y1[i-2]
             -a[1]*y2[i-1]-a[2]*y2[i-2])

for i in range(2,len(data)):
    b, a = iirnotch(f3/fs*lfo[i], Q)
    y3[i] = (b[0]*y2[i]+b[1]*y2[i-1]+b[2]*y2[i-2]
             -a[1]*y3[i-1]-a[2]*y3[i-2])

for i in range(2,len(data)):
    b, a = iirnotch(f4/fs*lfo[i], Q)
    #b, a = iirnotch(fc[i]/(fs/2), Q)
    y[i] = (b[0]*y3[i]+b[1]*y3[i-1]+b[2]*y3[i-2]
             -a[1]*y[i-1]-a[2]*y[i-2])
    
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/phasernotch3.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

out = y + g*data

#plot
plt.plot(time, data, 'g--', time, y, 'r--')
plt.title('Efecto Phaser')
plt.xlabel('datos verde, datos filtrados rojo')
plt.grid()
plt.show()
