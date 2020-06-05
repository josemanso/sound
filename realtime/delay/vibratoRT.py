#vibratoRT
import numpy as np
import pyaudio
import time

#  tipical delay, 5-10 ms, LFO 4-14 Hz

#la frecuencia de muestreo en tiempo real es un CHUNK
fs = 1024 # Hz
delay = 0.010*fs # 441 tramas
fo = 6 # Hz frec lfo
# real time
CHUNK = 1024 # valor por defecto pyaudio
index = np.arange(CHUNK)
lfo = np.sin(2*np.pi*index*fo/fs)

RATE = 44100
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #print('data ', len(data))
    # hacemos el computo
    y = np.zeros(len(data))
    for i in range(len(data)):
        M = (1+delay + delay * lfo[i])
        Mi = int(M)
        frac = M-Mi
        #primeros retardos han de ser positivos
        if (Mi+1) > i:
            Mi = i-1
        y[i] = data[i-(Mi+1)]*frac + data[i-Mi]*(1-frac)

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
