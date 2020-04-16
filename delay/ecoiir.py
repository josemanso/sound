import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
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
# IIR filter generate an infinite number of echoes with a = 0.8 for delay R =1000
#read wav file
fs, audio = wavfile.read(filename)
#normalizar datos entre -1 y 1: 2¹⁶ / 2 32768= 
#audio = audio/ 32768

# retardo > 50 ms  , 44100 Hz c/s * 50 10e-3= 2205 samples
M = 50000 # samples delay, un segundo
b = np.zeros(int(M/2))
b[0] = 1
#b[-1] = 1


a = np.zeros(M)
a[0] = 1
a[-1] = -0.4

data_filt = lfilter(b,a,audio)



# write wav file
wavfile.write('/home/josemo/python/wavfiles/eco.wav',fs,
              data_filt.astype(np.int16))
fs, data_eco = wavfile.read('/home/josemo/python/wavfiles/eco.wav')

plt.figure()
plt.title('Echo IIR')
plt.subplot(211)
plt.plot(audio, 'g--')
#plt.title('Echo IIR')
plt.subplot(212)
plt.plot(data_eco, 'r--')
plt.xlabel('Original soun, green; data_filter, red')


plt.show()

