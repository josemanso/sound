#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:02:57 2020

@author: josemo
"""

# respuesta impulso shelving
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
#from scipy.io import wavfile
from scipy.signal import freqz
import matplotlib.pyplot as plt

def shelving(G, fc, fs, Q, tipo):
    # All coefficients are calculated as described in Zolzer's DAFX book 
    #
    #G is the logrithmic gain (in dB)
    # FC is the center frequency
    # Fs is the sampling rate
    # Q adjusts the slope be replacing the sqrt(2) term
    # type is a character string defining filter type
    # Choices are: 'Base_Shelf' or 'Treble_Shelf'
    
    #if type == 'Base_self:
     #   base_self = true
    K = np.tan((np.pi * fc)/fs)
    V0 = 10**(G/20)
    root2 = 1/Q  
    # invertir ganacia para cut
    if(V0 < 1):
        V0 = 1/V0
    
    # Base Boots
    if (G > 0) & (tipo=='Base_Shelf'):
        
        b0 = (1 + np.sqrt(V0)*root2*K + V0*K**2) / (1+root2*K+K**2)
        b1 = (2 * (V0*K**2 -1)) / (1+root2*K+K**2)
        b2 = (1 - np.sqrt(V0)*root2*K + V0*K**2) / (1+root2*K+K**2)
        a1 = (2 * (K**2 - 1)) / (1+root2*K+K**2)
        a2 = (1 - root2*K + K**2) / (1+root2*K+K**2)
        
    # base cut
    elif(G < 0) & (tipo=='Base_Shelf'):
        
        b0 = (1 + root2*K + K**2) / (1 + root2*np.sqrt(V0)*K + V0*K**2)
        b1 = (2 * (K**2 - 1) ) / (1 + root2*np.sqrt(V0)*K + V0*K**2)
        b2 = (1 - root2*K + K**2) / (1 + root2*np.sqrt(V0)*K + V0*K**2)
        a1 = (2 * (V0*K**2 - 1) ) / (1 + root2*np.sqrt(V0)*K + V0*K**2)
        a2 = (1 - root2*np.sqrt(V0)*K +V0*K**2) / (1 + root2*np.sqrt(V0)*K + V0*K**2)
        
    # Treble boots, agudos
    elif(G > 0) & (tipo=='Treble_Shelf'):
        
        b0 = (V0 + root2*np.sqrt(V0)*K + K**2) / (1+root2*K+K**2)
        b1 = (2 * (K**2 - V0) )  / (1+root2*K+K**2)
        b2 = (V0 - root2*np.sqrt(V0)*K + K**2) / (1+root2*K+K**2)
        a1 = (2 * (K**2 - 1)) / (1+root2*K+K**2)
        a2 = (1 - root2*K + K**2) / (1+root2*K+K**2)
        
    # Treble cut
    elif(G < 0) & (tipo =='Treble_Shelf') :
        
        b0 = (1 + root2*K + K**2) / (V0 + root2*np.sqrt(V0)*K + K**2)
        b1 = (2 * (K**2 - 1) ) / (V0 + root2*np.sqrt(V0)*K + K**2)
        b2 = (1 - root2*K + K**2) / (V0 + root2*np.sqrt(V0)*K + K**2)
        a1 = (2 * (K**2/V0 - 1) ) / (1 + root2/np.sqrt(V0)*K + K**2/V0)
        a2 = (1 - root2/np.sqrt(V0)*K + K**2/V0) /(1 + root2/np.sqrt(V0)*K + K**2/V0)
    
    # allpass    
    else:
        b0 = V0
        b1 = 0
        b2 = 0
        a1 = 0
        a2 = 0
    # return values
    a = [1, a1, a2]
    b = [b0, b1, b2]
    print( 'el a ' , a, '  el b ' , b)
    return b,a

# filtro Shelving de 2º orden
# set Parameters for Shelving Filter 
G = -3
G1 = 3
fcl = 100
fch = 10000
Q = 0.6
#tipo = 'Base_Shelf'
fs = 44100

b1, a1 = shelving(G, fcl, fs, Q, tipo = 'Base_Shelf')
bh, ah = shelving(G, fch, fs, Q, tipo = 'Treble_Shelf')
b11, a11 = shelving(G1, fcl, fs, Q, tipo = 'Base_Shelf')
bh1, ah1 = shelving(G1, fch, fs, Q, tipo = 'Treble_Shelf')
#w, h = freqz(np.concatenate((bl)), np.concatenate((al,ah)))
w, h = freqz(b1, a1)
freq = w*fs/(2*np.pi)
w1, h1 = freqz(bh, ah)
w11, h11 = freqz(b11,a11)
wl1, hh1 = freqz(bh1,ah1)
#plot
#fig, ax = plt.subplots(2, 1, figsize=(8, 6))
fig, ax =plt.subplots()
ax.plot(h)
ax.plot(h1)
ax.plot(hh1)
ax.plot(h11)
#ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')

plt.title('Shelving filter')
plt.yscale("log")
plt.xscale("log")
plt.grid()
plt.show()