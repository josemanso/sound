import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
#from scipy import fftpack, signal
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
print('audioshape: ',audio.shape, ', array longitud \nlongitud: ',len(audio))
print('datos: \n', audio)
print(' tipo datos:', audio.dtype)
print(' tipo datos2: ', type(audio))

time = np.arange(len(audio))/Fs
plt.plot(time, audio)
plt.title('Wave form')
plt.xlabel('time, seconds')
plt.ylabel('Amplitud')

plt.show()
