#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:52:02 2020

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

def compressor(ind, xc, R, th, d, gain):
    rcomp = 1/R # ratio compressor
    d0 = th # threshold
    
    if abs(xc[ind]) >= abs(xc[ind-1]):
        d[ind] = d[ind-1] + abs(xc[ind])
    else:
        d[ind] = d[ind-1]
    # ganacia para comprimir
    if d[ind] >= d0:
        gain[ind] = (d[ind]/d0)**(rcomp-1)
    #else:
        #gain[ind] = 1
    #print('d compr ', d[ind], ' gain ', gain[ind])
        
def expander(ind, xe, Ra, thresh, d, gain):
    rexp = Ra+2
    d0 = thresh
    
    if abs(xe[ind-1] < 0.0001):
        # ruido
        gain[ind-1]=0
    else:
        if abs(xe[ind]<= abs(xe[ind-1])):
            d[ind] = d[ind-1] +abs(xe[ind])
            #d[ind] = d[ind-1]
        else:
            d[ind] = d[ind-1]
            #d[ind] = d[ind-1] +abs(xe[ind])
        #gain
        if d[ind] <= d0:
            #gain[ind] = (d[ind]/d0)**(rexp-1)
            gain[ind] = (d0/d[ind])**(rexp-1)
        
    #print('dexpander ', d[ind]/d0, ' gain ', gain[ind])


def comprexpander(x, ratio, th_compress, th_expan):
    # x data input
    # ratio  ratio conpressor 1/ratio, expander ratio
    # th  threshold
    
    th_c = 10**(th_compress/20)
    th_e = 10**(th_expan/20)
    d = np.zeros(len(x))
    gain = np.ones(len(x))
    out = np.zeros(len(x))
    out[0] = x[0]
    
    for i in range(1,len(x)):
        if abs(x[i]) > th_c:
            compressor(i, x, ratio, th_c, d, gain)
            
        elif (abs(x[i]) < th_e) and (abs(x[i]) > 0.0001):
            expander(i, x, ratio, th_e, d, gain)
        else:
            gain[i] =1
        out[i] = x[i]*gain[i]
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

# fuera de la curva con ganancia 1

datan = data / 32768  # 2¹⁶ /2
th_comp= -5 # dB
th_exp = -70 # dB
#attack = 0.1
#release = 0.94
CR = 4
#y = compexpander(datan, attack, release, CR, thComp, thExp)
y = comprexpander(datan, CR, th_comp, th_exp)

#threshold=0.01)

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