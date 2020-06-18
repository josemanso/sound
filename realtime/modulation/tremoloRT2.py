
#  tremolo en tiempo real
import numpy as np
import pyaudio
import time

# frecuencia moduladora
fo = 20#50
alpha = 0.5 # Amplitud, AM

# tiempo real
RATE = 44100
CHUNK = 1024

index = np.arange(0, CHUNK*8,1)
am = 1+alpha*np.sin(2*np.pi*index*(fo/RATE))
# tiene que variar a lo largo de más tiempo, por ejem 8
y = np.zeros(1024)
ind = 0
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    
    global ind
    tremolo = am[1024*ind:1024*(ind+1)]
    ind +=1
    if ind >7:
        ind = 0
   
   
    y = tremolo *data
    
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
