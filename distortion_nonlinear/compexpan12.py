#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 09:25:55 2021

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

#def comprexpander(x, ratio, t_ata, t_dec, th_compress, th_expan):
def comprexpander(x, ratio, th_compress, th_expan):
    # x data input
    # ratio  ratio conpressor 1/ratio, expander ratio
    # th  threshold
    # t_ata attack
    # t_cai release
    
    # para comparar con los valores de los datos 
    th_c = 10**(th_compress/20)*32769
    th_e = 10**(th_expan/20)*32769
    
    cn = np.zeros(len(x)) # detección de nivel
    gain = np.ones(len(x)) # ganacia
    out = np.zeros(len(x))
    out[0] = x[0]
    cn[0] = abs(x[0])
    
    for i in range(1,len(x)):
        cn[i] = abs(x[i])
        if abs(x[i]) > th_c:
            # compresión
            if abs(x[i]) > abs(x[i-1]) :
                #cn[i] = t_ata * cn[i-1] + (1- t_ata)*abs(x[i])
                cn[i] = abs(x[i]) # esto ya está
            else:
                cn[i] = cn[i-1]
            # proceso de ganacia f[c]   
            if cn[i] >= th_c :
                gain[i] =(cn[i] / th_c)**(1/ratio - 1)
            # si no la ganacia queda a 1
        elif abs(x[i]) < th_e :
            # expansor
            if abs(x[i]) > 1 :
                # si fuera menor, ruido  no expandir
            #else:
                # expandir
                if abs(x[i] <= abs(x[i - 1])):
                    #cn[i] = t_ata * cn[i-1] + (1- t_ata)*abs(x[i])
                    cn[i] = abs(x[i]) # echo
                else:
                    cn[i] = cn[i-1]
                # proceso de ganacia
                if cn[i] <= th_e :
                    gain[i] = (cn[i] / th_e)**(ratio -1)
                # sino queda a 1
        else:
            gain[i] = 1
        # fin del proceso de ganacias
        #plt.plot(cn)
        #plt.show()
        out[i] = x[i] * gain[i]
    plt.plot(gain)#[:4000])
    plt.show()
  
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

#datan = data / 32768  # 2¹⁶ /2
th_comp= -10#-5 # dB
th_exp = -50#-70 # dB
#attack = 0.9#0.09 #0.1
#release = 0.94 #0.094
CR = 4
#y = compexpander(datan, attack, release, CR, thComp, thExp)
y = comprexpander(data, CR, th_comp, th_exp)
#y = comprexpander(datan, CR, attack, release, th_comp, th_exp)

#threshold=0.01)

#y = y * 32768
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/comprexpander2.wav',
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

#plt.figure(3)
#plt.plot(time,gain)
#plt.ylabel("log")
#plt.grid()


plt.show()