import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq, rfft
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "grabacion.wav"
        
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
    
#

Fs, audio = wavfile.read(filename)
print('frequencia: ', Fs,'Hz')
print('audioshape: ',audio.shape, ', array longitud\nlongitud: ',len(audio))
#print(f"number of channels = {audio.shape[1]}")
print('datos: \n', audio)

datafft = fft(audio)
# abs
fftabs = np.abs(datafft)
freqs = fftfreq(len(audio), 1/Fs)
#plt.subplot(2,1,1)
#time = np.arange(len(audio))/Fs
#plt.plot(time, audio)
plt.figure(1)
plt.title('FFT')
plt.xlim( [10, Fs/2] )
plt.xscale('log')
plt.grid(True)
plt.xlabel('Frecuencia, Hz')
plt.ylabel('Magnitud')
plt.plot(freqs[:int(freqs.size/2)], fftabs[:int(freqs.size/2)])

# plt.subplot(2,1,2)
plt.figure(2)
fft_rfft = abs(rfft(audio))
fft_db = 20*np.log10(fft_rfft)
# normalise to 0 dB max
fft_db -= max(fft_db)
plt.xscale('log')
plt.plot(freqs[:int(freqs.size/2)], fft_db[:int(freqs.size/2)])
plt.title('FFT-dB')
plt.xlabel('frecuencia, Hz')
plt.ylabel('Magnitud, (dB)')
plt.grid(True)

plt.show()
