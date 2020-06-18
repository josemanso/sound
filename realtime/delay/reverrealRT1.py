#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:54:03 2020

@author: josemo
"""
# real reverb multy delays
import os
import sys
import numpy as np
import pyaudio
import time
import queue as queue

RATE = 44100 # necesitamso 4 chunks, 1024 *4 = 

max_delay = 3515 # necesitamso 4 chunks, 3515/1024 = 3,43
q= queue.Queue(4)
q1= queue.Queue(4)
#cola = np.array([])
cola = np.zeros(1024*4)
def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
    # esperamos a tener 4 chunks, datas
    
    q.put(data)
    
    if q.full():
        cola1=q.get()
        # empiezamos a computar los ecos
        cola[1024*3:] = cola1
        #cola = [x*g for x in cola]
        for i in range(1024):
            samples = data.copy()
            samples[i] = (cola[i]+0.8*cola[i-190]+0.5*cola[i-940]
                       +0.49*cola[i-993]+0.37*cola[1-1183]+
                          0.38*cola[i-1192]+0.34*cola[i-1315]+
                          0.28*cola[2021]+0.27*cola[i-2140]+
                          0.19*cola[i-2524]+0.18*cola[i-2700]+
                          0.178*cola[i-3119]+0.142*cola[i-3268])
            # 0.8 +.....= 4.2+1
        samples = samples/5.5
    
    samples = np.array(data, dtype='int16')
    return (samples, pyaudio.paContinue)


p = pyaudio.PyAudio()
## open stream
stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
        stream_callback = callback)

stream.start_stream()
try:
    while stream.is_active():
        print("Stream is active")
        time.sleep(10)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    

stream.stop_stream()
stream.close()

p.terminate()