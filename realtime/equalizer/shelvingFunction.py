#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:59:22 2020

@author: josemo
"""

# función shelving

import numpy as np


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
    #print( 'el a ' , a, '  el b ' , b)
    return b,a
