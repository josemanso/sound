# Doubling o doubletraking con FIR
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "yooh.wav"
        
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
# read wave file
fs, data = wavfile.read(filename)

#El efecto doubling o doubletracking consiste en añadir una versión
# retardada muy pocos milisegundos al audio original
# (0< τ ≤ 10 milisegundos). 

delay = 280 #  5 ms 220 tramas
b = np.zeros(delay)
b[0]= 1
b[-1]= 0.7

data_filt = lfilter(b, 1, data)# sale muy saturado
data_filt =  data_filt/2

# write wav file
wavfile.write('/home/josemo/python/wavfiles/double.wav',
              fs, data_filt.astype(np.int16))
fs1, data1 = wavfile.read('/home/josemo/python/wavfiles/double.wav')

#plot
plt.figure()
time = np.arange(len(data))/fs
plt.plot(time, data, 'g--', time, data1, 'r--')
plt.title('Double tracking effect')
plt.xlabel('Origin green, filtered red')
plt.show()
