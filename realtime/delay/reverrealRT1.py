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
#import queue as queue

RATE = 44100 # necesitamso 4 chunks, 1024 *4 = 

max_delay = 3515 # necesitamso 4 chunks, 3515/1024 = 3,43
#q= queue.Queue(4)
#q1= queue.Queue(4)
#cola = np.array([])
#cola = np.zeros(1024*4)
cola = []
def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
    global cola
    # esperamos a tener 4 chunks, datas
    cola = np.append(cola, data)
    #q.put(data)
    if len(cola) ==(1024*4):
    #if q.full():
        #cola1=q.get()
        # empiezamos a computar los ecos
        #cola[1024*3:] = cola1
        #cola = [x*g for x in cola]
        for i in range(1024):
            samples = data.copy()
            ind = i+1024*3
            samples[i] = (cola[ind]+0.8*cola[ind-190]+0.5*cola[ind-940]
                          +0.49*cola[ind-993]+0.37*cola[ind-1183]+
                          0.38*cola[ind-1192]+0.34*cola[ind-1315]+
                          0.28*cola[ind-2021]+0.27*cola[ind-2140]+
                          0.19*cola[ind-2524]+0.18*cola[ind-2700]+
                          0.178*cola[ind-3119]+0.142*cola[ind-3268])
            # 0.8 +.....= 4.2+1
        samples = samples/5.5
    # quitamos 1024, un chunk, de la cola
    cola = cola[1204:]
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