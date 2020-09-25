#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:06:38 2020

@author: josemo
"""

import pyaudio
import time

#WIDTH = 2
#CHUNK = 1024
RATE = 44100


pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    #data = numpy.frombuffer(data)
    return (in_data, pyaudio.paContinue)

stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate = RATE,
                 input=True,
                 output=True,
                 stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(10)
    stream.stop_stream()
    print("Stream is stopped")
    
stream.close()

pa.terminate
    