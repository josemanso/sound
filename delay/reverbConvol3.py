# conlvolve reverberation
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
    
    
# Reverberation por comvolución

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

def fconv(x,h):
    ly = len(x)+len(h) -1
   
    X = fft(x, ly)
    H = fft(h, ly)
    
    Y = X * H  # convolution
    y = np.real(ifft(Y,ly))
    y=y/max(abs(y))
    return y


# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# tomamos el archivo de respuesta a impulso
#fsIr, IR = wavfile.read("/home/josemo/impulse_room.wav")
#fsIr, IR = wavfile.read("/home/josemo/impulse_cathedral.wav")
fsIr, IR = wavfile.read("/home/josemo/python/wavfiles/IR/church.wav")
#fsIr, IR = wavfile.read("/home/josemo/python/wavfiles/reverbIR11.wav")
print('data IR ', IR.shape, ' fs ', fsIr)
tr = np.arange(len(IR))/fsIr
plt.figure(1)
plt.plot(tr, IR)
plt.title('Impulse response')

# normalizamos entre -1 y 1
datan = data/2**15
IRn = IR/2**15
y = fconv(datan,IR)
y = y * 2**15
# write wav file

try:
    wavfile.write('/home/josemo/python/wavfiles/reverbConvchur1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
plt.figure(2)
time = np.arange(len(data))/fs
plt.subplot(211)
timerv= np.arange(len(y))/fs
plt.plot(timerv, y)
#plt.plot(y,'r--', data,'g--')
plt.title("Convolution Reverb")
plt.xlabel(' ')
#plt.plot(time, y, 'r--',time, data,'g--')
plt.subplot(212)
plt.plot(time, data)
plt.title("original")

#plt.xlabel('Original green, reverb red')

plt.show()
    