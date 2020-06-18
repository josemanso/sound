#  Ring en tiempo real
import numpy as np
import pyaudio
import time

# Efecto RING modulación, señal seno
fc = 300 #200

# tiempo real
RATE = 44100
CHUNK = 1024

index = np.arange(0, CHUNK,1)
carrier = np.sin(2*np.pi*index*fc/RATE)# modulación

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    
    # hacemos el computo
    y = carrier *data
    sample = y.astype(np.int16).tostring()
    
    return (sample, pyaudio.paContinue)

# open stream
stream = pa.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
        stream_callback = callback)
stream.start_stream()

while stream.is_active():
    print("Stream is active")
    time.sleep(10)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()
