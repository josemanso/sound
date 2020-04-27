# ecualizador paramétrico
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt

from peakfunction1 import peakfilter
from shelvingFunction import shelving

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

# filtro Shelving de 2º orden
# set Parameters for Shelving Filter
fs = 44100
Q = 0.7
#tipo = 'Base_Shelf'  'Treble_Shelf'
# llamada a la función shelving

bb, ab = shelving(-3, 100, fs, Q, tipo = 'Base_Shelf')
bh, ah = shelving(-1, 8000, fs, Q, tipo = 'Treble_Shelf')
#
# filtro peak 2º orden
# llamada a la funcio peak
b,a = peakfilter(-1, 180,fs,Q)
b1,a1 = peakfilter(1, 540,fs,Q)
b2,a2 = peakfilter(2, 1620,fs,Q)
b3,a3 = peakfilter(3, 4860,fs,Q)

# filtramos la señal
#filtro shelving graves
sl = lfilter(bb, ab, data)
#filtro peak menos frecuencia central, o de corte
pa1 = lfilter(a,b,sl)
#segundo peak
pa2 = lfilter(b1,a1, pa1)
# 3º
pa3 = lfilter(b2,a2, pa2)
# 4º
pa4 = lfilter(b3,a3, pa3)
# y el shelving graves
y = lfilter(bh,ah, pa4)

y[y>32768] = 32767
y[y<-32768] = -32767

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/ecualizabandas.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
time = np.arange(len(data))/fs
plt.plot(time, y, 'r--', time, data,'g--')#,time, data,'g--')
#plt.plot(time, data, 'g--', time, y,'r--')#,time, data,'g--')
plt.title('Ecualizador parámétrico')
plt.xlabel('Original green, filtrada red')
plt.show()


