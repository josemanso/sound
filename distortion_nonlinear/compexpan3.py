#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:09:00 2020

@author: josemo
"""

# Compresor expansor
# Compressor Expander
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def absdecibel(d):
    dby = np.zeros(len(data))
    for i in range(len(data)):
        x = np.abs(data[i])
        if x <= 0.0001:
            dby[i] = -90
        else:
            dby[i] = 20*np.log10(x/ 32767)
    return dby

def compressor(ind, x, attack, release, CR, threshold, d, gain):
    
    rcomp = 1/CR # compressor
    d0 = threshold # umbral deseado
    # detección de este valor instantáneo
    if np.abs(x[ind]) >= np.abs(x[ind-1]):
        d[ind] = attack*d[ind-1] +(1-attack)*np.abs(x[ind])
    else:
        d[ind] = release*d[ind-1]
    # ganancia compressor
    if d[ind]>= d0:
        gain[ind] = d[ind]/(d0+1e-15)**(rcomp-1)
    else:
        gain[ind] = 1
        
def expander(ind, x, attack, release, CR, threshold, d, gain):
    #print('expander')
    d0 = threshold # umbral deseado
    # detección de este valor instantáneo
    if np.abs(x[ind]) <= np.abs(x[ind-1]):
        d[ind] = attack*d[ind-1] +(1-attack)*np.abs(x[ind])
    else:
        d[ind] = release*d[ind-1]
    # ganancia expansor
    rexp = CR
    if d[ind]>= d0:
        gain[ind] = 1
    else:
        gain[ind] = d[ind]/(d0+1e-15)**(rexp-1)
    

def compexpander(x, attack, release, CR, threshold):
    # x :input signal
    # fs :samplerate
    # attack: attack time constant (fast)/ forgetting factor
    # release: release time constant (slow)
    # CR = Compressor ratio
    
    # threshol es el umbral deseado = 0.01
    # attack  =  0.1, release  =  0.97,  CR  =  4  and  d0  =  0.01
    

    # 1st separar la señal que hay que compromir, de la quehay que expandir
    # Nivel compresión más de -3db
    # nivel expandir mas de - 80 dB, ruido no lo miro aqui
    # dB = 20*log(dato/32678) de 0 a -90
    
    d = np.zeros(len(x)) # datos de comparación de los valores instantaneos
    gain = np.zeros(len(x)) # la ganancia para cada trama
    out = np.zeros(len(x)) # la salida que obtendremos
    
    dB = absdecibel(x)
    for i in range(len(x)):
        if dB[i] > -10: #-3:
            compressor(i,x, attack, release, CR, threshold, d, gain)
        elif dB[i] < -70: #-80:
            expander(i, x,attack, release, CR, threshold, d, gain)
        else:
            gain[i] =1
            
        out[i] = gain[i]*x[i]
    return out
    

          

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "fish.wav"
        
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
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# fuera de la curva con ganancia 1
#d = np.zeros(len(x))
#gain = np.zeros(len(x))
#out = np.zeros(len(x))
datan = data / 32768  # 2¹⁶ /2
y = compexpander(datan, attack=0.1, release=0.94, CR=4, threshold=0.01)

y = y * 32768
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/comprexpander1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)    
#plot
time = np.arange(len(data))/fs
plt.figure(1)
#plt.subplot(211)
plt.plot(time, y, 'r--', time, data,'g--')
#plt.subplot(212)
plt.figure(2)
# máx alrededor de 3.6, antes

plt.plot(time,data, 'g--',time,y, 'r--')
#plt.ylabel("log")
plt.grid()
plt.show()