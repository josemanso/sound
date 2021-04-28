# wah peak filter
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import iirpeak #, sawtooth
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

#time = np.arange(len(data))/fs

cut_min = 500    # LFO minval, Hz
cut_max = 3000   # LFO maxval, Hz
fw =  2000       # wah frecuency,
# cetro de la frecuencia
delta = fw/fs

depth = 2   # factor Q, filter iirpeak fw/fs

# crear una onda triangular con los valores de frecuencias
fc = []
while (len(fc)<len(data)):
    fc = np.append(fc, np.arange(cut_min, cut_max, delta))
    fc = np.append(fc, np.arange(cut_max, cut_min, -delta))
# quitamos lo qe sobra
fc = fc[:len(data)]
# fc es el LFO
    
y = np.zeros(len(data))

for i in range(2,len(data)):
    b, a = iirpeak(fc[i]/(fs/2), depth)
    y[i] = (b[0]*data[i] + b[1]*data[i-1]+ b[2]*data[i-2]
            -a[1]*y[i-1]-a[2]*y[i-2])
            
gain = 0.8

yout = (1-gain)*data +  gain*y
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/wahwah2.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
    
# read wave file
filein = '/home/josemo/python/wavfiles/wahwah1.wav'
fs, data1 = wavfile.read(filein)
            
#plot

time = np.arange(len(data))/fs

plt.plot(time,data, 'g--', time, y,'r--')
#plt.plot(time, fc)
plt.title('Efecto wah-wah')
#plt.xlabel('señal original verde, señal filtrada rojo')
plt.xlabel('tiempo')

plt.show()
 