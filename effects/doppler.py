import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import lfilter

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
print(' fs', fs,' shapes ', data.shape, ' data ', data)
data= data[:5*fs] # acortamos a 5 segundos
#data= data[:3*fs] # acortamos a 5 segundos
# doppler

Vsonido = 342.0 # m/seg

S = 27 # velocidad de la fuente m/seg

b = 50 # distancia del observador a la fuente, ortogonal

# ventana de observación entre 60º - 0º - 60º
# distancia a recorrer por la fuente cos 60 = 0.5, serian 25 metros x 2
# radianes = 2pi
# Vr = S x cos theta
phi = np.arange(61)
rphi = phi[::-1]

SRac = S * np.cos(rphi* np.pi/180)  # 60º hasta llegar a 0º
SRal = S * np.cos(phi*np.pi/180)
# alejarse + y acercar f’ = f(vs/ vs-V/2)
foac = fs*(Vsonido / (Vsonido - SRac))
#print('foac obsrv acercarse ', foac) 
foal = fs*(Vsonido / (Vsonido + SRal))

# lo vamos a dividor entre 120 observaciones

buffer = 50 # tramas


# modificar el tiempo de retardo entre la fuente y el receptor
b =[]
for i in range(122):
    #primera parte de 0.5 a 1
    if i <= 122//2-1:
        fn = foac[i]
        
    else:
        fn = foal[i-122//2]
    
    x = fn*buffer/fs
    
    delay = np.round(x)
    delay = int(delay)
    #print(' delay ', delay)
    bi = np.zeros(delay)
    #bi[0] = bi[-1] = 1
    bi[-1] = 1
    b = np.append(b, bi)
    
y = lfilter(b, 1, data) 
        
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/doppler.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)      

#fig = plt.figure(1, figsize =(8,3))
#ax = fig .add_subplot(1,2,1)
plt.subplot(1,2,1)
plt.plot(y)
plt.title('Efecto doppler')

plt.subplot(1,2,2)
plt.title('Señal original')
plt.plot(data[:5*fs])
plt.show()
