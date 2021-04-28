# phaser o phasing
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
#from scipy.signal import sawtooth
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




# f1 = 300 # frecuencias de corte
#f2 = 800
#f3 = 1000
#f4 = 4000

g = 0.9


#phaseModulator = np.cos(2*np.pi*flfo*time/fs)
# mim and max centre cutoff frequency of variable bandpass filter
cut_min = 500
cut_max = 3000
# phaser frecquency
fw = 2000
# change in centre frequency per sample
delta = fw/fs

#depth = 2   # factor Q, filter iirpeak fw/fs
# crear una onda triangular con los valores de frecuencias
fc = []
while (len(fc)<len(data)):
    fc = np.append(fc, np.arange(cut_min, cut_max, delta))
    fc = np.append(fc, np.arange(cut_max, cut_min, -delta))
# quitamos lo qe sobra
fc = fc[:len(data)]

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
F1 = np.zeros(len(data))
for i in range(len(data)):
    F1[i] = 2*np.sin((np.pi*fc[i]/fs))
    
# size of notch
Q1 =0.2#0.5# 2# 1# 0.1 #2*0.05
yh = np.zeros(len(data))
yl = np.zeros(len(data))
yb = np.zeros(len(data))
yn = np.zeros(len(data))
# inicio
yh[0] = data[0]
yb[0] = F1[0] * yh[0]
yl[0] = F1[0] * yb[0]
yn[0] = yh[0] + yl[0]

for n in range(1,len(data)):
    yh[n] = data[n] - yl[n-1] - Q1*yb[n-1]
    yb[n] = F1[n] * yh[n] + yb[n-1]
    yl[n] = F1[n] * yb[n] + yl[n-1]
    yn[n] = yh[n] + yl[n]
    
    
    
# write wav file
out = (yn/2 + g*data)/1.5
wah =  (yb/2 + g*data)/1.5

try:
    wavfile.write('/home/josemo/python/wavfiles/phaser3.wav',
                       fs, out.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)



    
#plot
plt.plot(time, data, 'g--', time, out, 'r--')
plt.title('Efecto Phaser')
plt.xlabel('datos verde, datos filtrados rojo')
plt.grid()
plt.show()
