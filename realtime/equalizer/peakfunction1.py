#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 09:44:58 2020

@author: josemo
"""
import numpy as np

# peak filter for EQ
# peak filter for EQ
def peakfilter(G, fc, fs, Q):
    K = np.tan(np.pi*fc/fs)
    V = 10**(G/20)
    #b0 = (V + np.sqrt(2*V)*K+(K**2))/(1+np.sqrt(2)*K+K**2)
    b0 = (1 +(V/Q)*K + K**2)/(1 + (K/Q) + K**2)
    b1 = (2*((K**2)-1))/(1 + K/Q + K**2)
    b2 = (1 - (V/Q)*K + K**2)/ (1 + K/Q + K**2)
    a1 = (2*((K**2)-1))/(1 + K/Q + K**2)
    a2 = (1-(K/Q) + (K**2))/(1 + K/Q + K**2)
    A = [1, a1, a2] 
    B = [b0, b1, b2]
    #print('peak a ', A, ' b',B)
    return B,A
