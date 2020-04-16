# phaser o phasing
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

time = np.arange(len(data))/fs


flfo = 15

f1 = 300 # frecuencias de corte
f2 = 800
f3 = 1000
f4 = 4000
r1 = 0.9
r2 = 0.98
r3 = 0.8
r4 = 0.9
AP1a2 = r1**2
AP2a2 = r2**2
AP3a2 = r3**2
AP4a2 = r4**2
g = 0.9


#phaseModulator = np.cos(2*np.pi*flfo*time/fs)
phaseModulator = 0.8+sawtooth(2*np.pi*flfo*time)

y1 = np.zeros(len(data))
y2 = np.zeros(len(data))
y3 = np.zeros(len(data))
y = np.zeros(len(data))
#y = np.zeros(len(data))


for i in range(2,len(data)):
    
    theta1 = (1/fs)*f1*(1+phaseModulator[i])
    theta2 = (1/fs)*f2*(1+phaseModulator[i])
    theta3 = (1/fs)*f3*(1+phaseModulator[i])
    theta4 = (1/fs)*f4*(1+phaseModulator[i])
    
    AP1a1 = -2*r1*np.cos(theta1)
    AP2a1 = -2*r2*np.cos(theta2)
    AP3a1 = -2*r3*np.cos(theta3)
    AP4a1 = -2*r4*np.cos(theta4)
    
    # Applies each filter using the difference equations
    y1[i] = (AP1a2*data[i]+AP1a1*data[i-1]+data[i-2]
            -AP1a1*y1[i-1] - AP1a2*y1[i-2])
    y2[i] = (AP2a2*y1[i]+AP2a1*y1[i-1]+y1[i-2]
            -AP2a1*y2[i-1] - AP2a2*y2[i-2])
    y3[i] = (AP3a2*y2[i]+AP3a1*y2[i-1]+y2[i-2]
            -AP3a1*y3[i-1] - AP3a2*y3[i-2])
    y[i] = (AP4a2*y3[i]+AP4a1*y3[i-1]+y3[i-2]
            -AP4a1*y[i-1] - AP4a2*y[i-2])

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/phaser2.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

out = y + g*data

    
#plot
plt.plot(time, data, 'g--', time, y, 'r--')
plt.title('Efecto Phaser')
plt.xlabel('datos verde, datos filtrados rojo')
plt.grid()
plt.show()
