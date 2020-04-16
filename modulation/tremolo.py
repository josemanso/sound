# Tremolo
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
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

fo = 5  # frecuencia moduladora
alpha = 0.9  # amplitud AM
y = np.zeros(len(data))
for i in range(len(data)):
    y[i] = (1+alpha*np.sin(2*np.pi*i*(fo/fs))) * data[i]
    
y = y/2

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/tremolo.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
# write wav file
#wavfile.write('/home/josemo/python/wavfiles/reverb1.wav', fs, y.astype(np.int16))

#plot
time = np.arange(len(data))/fs
plt.plot(time, data,'g--', time, y, 'r--')
plt.title("Tremolo")
plt.xlabel('Original green, tremolo red')
plt.show()
