# Falging effect
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "acoustic.wav"
        
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

# y[n] = g1 x [n] + g2 x[n- M(n)]  
# M(n) = M0(1 + Asin2pifnT)
# f es la frecuencia que marca la velocidad de flanging.  
# A es el valor máximo de variación del tiempo de retardo respecto a M0 
# M0 es el valor medio del tiempo de retardo. 
# Los valores habituales de M0 están entre 0 y 15 milisegundos
# feedback, gff =0.8 gfb = 0.5
# y[n] = gfb y[n-M[n]] + x[n] + (gff-gfb)x[n-M[n]]


max_time_delay = 133 # 3 ms
rate = 0.2 # frecuencia lfo
gff = 0.7 # ganancia a la salida
gfb = 0.5 # ganancia en la realimentación delay, ffedback

index = np.arange(len(data))
sin_ref = np.sin(2*np.pi*index*(rate/fs))
y = np.zeros(len(data))
y[:max_time_delay] = data[:max_time_delay] # = np.copy(data)

for i in range (max_time_delay +1, len(data)):

    lfo = np.abs(sin_ref[i]) # valores entre 0 y 1
    delay = max_time_delay * lfo
    delay = int(delay)
     
    #y[i] = (0.7*data[i] +  0.7*data[i-delay])/2
    # y[n] = gfb y[n-M[n]] + x[n] + (gff-gfb)x[n-M[n]]
    y[i] = gfb*y[i-delay] + data[i] + (gff - gfb)*data[i-delay]/4
    if y[i] >= 32768: # para quitar algunas tramas de mayor valor
        y[i] = 32765
    elif y[i]<= -32768:
        y[i] = -32768
    
    

# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/flanger.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
    
#fs1, data1 = wavfile.read('/home/josemo/python/wavfiles/flanger.wav')

#plot
#f, ax1 = plt.subplots(1,1,figsize=(8,5))
plt.figure(figsize=(8,5))
time = np.arange(len(data))/fs
plt.plot(time, y, 'r--',time, data,'g--')
plt.title('Flanger')
plt.xlabel('Rojo datos flanging, verde, audio original')
#ax1[1].plot(time, data, 'g--', time, data1, 'r--')
plt.show()

