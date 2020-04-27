#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:43:32 2020

@author: josemo
"""

#plot función distorsión fuz hard clippin ccrma.standford.edu
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

def distorfuzz(x, g): 
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))

    return y
    
    

x = np.array([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6,0.8,1])
y = np.zeros(len(x))

g = 10
y = distorfuzz(x,g)


print('y ', y)


        
plt.plot(x,y, label= "gain = 10")
plt.legend()
plt.title('Curva distorsión/fuzz simétrico')
plt.ylabel('output')
plt.xlabel('input')

plt.grid()
            
plt.show()