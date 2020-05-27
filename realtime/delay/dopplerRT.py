# doppler, en tiempo real
import numpy as np
import pyaudio
import time
import queue as queue

# doppler
#RATE = 44100
fs = 44100

Vsonido = 342.0 # m/seg

S = 27 # velocidad de la fuente m/seg

b = 50 # m distancia del observador a la fuente, ortogonal
# usaremos b como valor del buffer de delay
# ventana de observación entre 60º - 0º - 60º
# 44 observaciones en cada sentido 0--43 y 43--0
phi = np.arange(61)
rphi = phi[::-1]

SRac = S * np.cos(rphi* np.pi/180)  # 60º hasta llegar a 0º

SRal = S * np.cos(phi*np.pi/180)

foac = fs*(Vsonido / (Vsonido - SRac))# acercarse
foal = fs*(Vsonido / (Vsonido + SRal))# alejarse

# 2 segundos acercandose y 2 s alejandose,2s = 86 CHUNK (1024)


RATE = 44100
pa= pyaudio.PyAudio()

t = time.time()
# tenemos frame count
count = 0
q = queue.Queue(1)
aux = np.zeros(1024)
q.put(aux)

def callback(in_data, frame_count, time_info, status):
   
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    # hacemos el computo
    global count
    
  
    y = np.zeros(len(data))
    if count <61:
        # acercandose
        fn = foac[count]
    elif count < 61*2:
        fn = foal[count-61]
    else:
        fn = RATE/b
    count += 1 # count +1
    print('count ', count)
    # delay
    x = fn*b/RATE
    delay = np.round(x)
    delay = int(delay)
    print('delay ', delay)
    # función de tranferencia FIR orden 1 y[n] = x[n-delay]
    # hay que recordar el anterior
    sample = q.get()
    for i in range(1024):
        if i -delay <0:
            y[i] = sample[1024+i-delay]
        else:
            y[i] = data [i-delay]
    
    q.put(data)
    data_out = y.astype(np.int16).tostring()
    return(data_out, pyaudio.paContinue)
    #return (sample, pyaudio.paContinue)

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
    time.sleep(3)
    stream.stop_stream()
    print("Stream is stopped")

#stream.stop_stream()
stream.close()

pa.terminate()
