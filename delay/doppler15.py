import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "ambulancia1.wav"
        
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
#print(' fs', fs,' shapes ', data.shape, ' data ', data)
data= data[:5*fs] # acortamos a 5 segundos
print(' fs', fs,' shapes ', data.shape, ' data ', data)

S = 27 # velocidad de la fuente m/seg
Vsonido = 342.0 # m/seg
g = S/Vsonido
print('g ', g)# 0,0789, 1-g = 092

L = len(data)
delay = np.zeros(len(data))
# hay que hacerlo desde g = 0
for h in range(L//2, 0, -1):
    #delay2[h-1] = delay2[h]+(1-g)
    delay[h-1] = delay[h]+g
for j in range(L//2, L-1):
    #delay2[j+1] = delay2[j]+(1-g)
    delay[j+1] = delay[j]+(g)

inicio = int(delay[0])
yout = np.zeros(len(data))
for k in range(inicio,len(data)):
    # interpolación
    #rpi = np.floor(delay[k])
    #print('rpi ', rpi)
    rpi = int(delay[k])
    a = delay[k] - rpi
    #print(' a ', a)
    yout[k] = a*data[k-rpi+1] +(1-a)*data[k-rpi]
    #yout[k] = data[k-rpi]

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/dopplerD.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)      

#fig = plt.figure(1, figsize =(8,3))
#ax = fig .add_subplot(1,2,1)
plt.subplot(2,1,1)
plt.plot(data, 'g--', yout, 'r--')
plt.title('Efecto doppler')

plt.subplot(2,1,2)
plt.ylabel('delay')
plt.plot(delay)
plt.show()
  