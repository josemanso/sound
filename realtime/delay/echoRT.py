#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:30:22 2020

@author: josemo
"""

# eco 
import os
import numpy as np
import pyaudio
import time
import queue as queue

RATE = 44100
# 1024*25 = 25600 
q = queue.Queue(25)

def callback(in_data, frame_count, tiem_info, status):
    data = np.frombuffer(in_data, np.int16 )
    # esperamos un tiempo o un nº de frames 
    q.put(data)
    if q.full():
        #print('Full')
        cola = q.get()
        #print('lon ', len(cola) ,'y shape ',cola.shape, 'typo', cola.type )
        #cola = map(lambda x: x*0.4, cola)
        cola = [x*0.4 for x in cola]
        data = data + cola  
        data = np.array(data, dtype='int16')
    return (data, pyaudio.paContinue)

    
p= pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),# un bytes
                channels=1,
                rate= RATE,
                input=True,
                output=True,
                stream_callback =callback)

stream.start_stream()

try:
    while stream.is_active():
        print("Stream is active")
        time.sleep(10)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    
stream.close()
p.terminate()