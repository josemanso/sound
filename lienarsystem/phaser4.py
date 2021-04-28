# phaser o phasing, similaraflanger
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import sawtooth
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
print(' type ', data.dtype)
data = data.astype(np.int32)
print(' type ', data.dtype)
time = np.arange(len(data))/fs
#index = np.arange(len(data))

#delay entre 1 - 10 ms; fs 44100son entre 44 y 441
# con el 10 del lfo está puesto el retardo

# parecido a flanger, cambindo el lfo, con una un señal diente de sierra
f_lfo = 0.5 # menor de 1 Hz
# crear una onda diente de sierra
#index = np.arange(0,1024,1)
lfo = abs(np.round(10* sawtooth(2 *np.pi * f_lfo *time)))# abs
lfo = lfo.astype(np.int16)
#lfo = 10* sawtooth(2 *np.pi * f_lfo *index/fs)# abs
# se necesita un número entero y positivo de tranmas

#lfo = abs(lfo)
#print('lfo ', lfo.dtype, ' val ', lfo)
#lfo = int(lfo)
plt.plot(lfo)
plt.show()

# f1 = 300 # frecuencias de corte
#f2 = 800
#f3 = 1000
#f4 = 4000
y = np.zeros(len(data))
#y[:max_time_delay] = data[:max_time_delay]
g = 0.9


#phaseModulator = np.cos(2*np.pi*flfo*time/fs)
# mim and max centre cutoff frequency of variable bandpass filter
#cut_min = 500
#cut_max = 2000
# phaser frecquency
#fw = 10000 # 2000central freq.
# change in centre frequency per sample
#delta = fw/fs

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


for n in range(44,len(data)):
    #M = round(lfo[n])
    #M = abs(M)
    #M = lfo[n]
    #if n%1000 ==0:
        #print('? M ', M.type, ' m val ', M)
        #print('? M  m val ', M)
    #M = int(lfo[n])
    #M = int(M)
    #y[n] = data[n] + data[n - M]
    M = data[n - lfo[n]]
    
    y[n] = data[n] + M
    #y[n] = data[n] + data[n - lfo[n]]
    #if n%10000 ==0:
    #if (data[n] > 0 and M < 0):
        #print('? M ', type(M), ' m val ', M, ' data ', data[n])
        #print('? M  m val ', M)
    
    
# write wav file
out = (y + g*data)/2

try:
    wavfile.write('/home/josemo/python/wavfiles/phaser4.wav',
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
