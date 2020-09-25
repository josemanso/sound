# Susbtracción espectral del ruido
import sys
import os
import numpy as np
import pyaudio
import time
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
from scipy.signal import hann


# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "grabacion.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/josemo/python/wavfiles/"+file_input):
    filename ="/home/josemo/python/wavfiles/"+file_input
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()    
# read wave file
fs, datan = wavfile.read(filename)
print('data ', datan.shape, ' fs ', fs)

RATE = fs

# ruido: el primer segundo del archivo 1024 *43 =44032
#noise = data[:44032] #  1 segundo aprox
# hHann window
hann_win = hann(1024)
# fft con hann_win y overlap al ruido
# overlap 50% , será 43*2 + 1 = 87
lps = int(44032/1024) +1
samplesn = np.zeros(1024) # []
noise_fft = [[]]

for i in range(lps*2):
    
    f_loc = int(i*1024/2) 
    
    samplesn = datan[f_loc:f_loc+1024]
    
    samplesn = samplesn*hann_win[:len(samplesn)]
    
    noise_fft.append(np.array(abs(fft(samplesn))))

noise = np.array(noise_fft[1])


    
for j in range(1, (lps*2)):
    
    noise = list(map(lambda x, y : x + y, noise, noise_fft[j]))
    
noise = list(map(lambda x: x/(lps*2), noise))
noise = np.mean(noise)

noise *= 7

print('noise ', noise)



# necesito 3 chunks, desde el segundo hacer el algoritmo
def noiseless(data_in):
    # tenemos noise, que es el ruido medio
    # signal_in, señal de entrada, para quitarla el ruido de fondo
    
    # tenemos la ventana hann - hann_win
    # la señal ha de ser de 1024, pero tengo tres tramas
    # necesito tres tramas con overlap del 50%,
    
    
    samples = np.zeros((3,1024)) # lista de tramas con overlap 50%
    

    phases = np.zeros((3, 1024)) # lista conr la infomación de la fase de cada trama
   
    # 1º hacer el overlap del 50 %
    for k in range(3):  
        samples[k] = data_in[(k+1)*512:(k+1)*512+1024]
        #windowing
        samples[k] = samples[k] * hann_win
        # fft
        samples[k] = fft(samples[k])
        phases[k] = np.angle(samples[k])
        samples[k] = abs(samples[k])
        
    
    # quitamos el ruido, spectral substraction
    samples = [list(map(lambda x : x - noise, l)) for l in samples]
    
    # quitamos los valores negativos, rectificado
    for idx, frm in enumerate(samples):
        samples[idx] = [0 if h < noise else h for h in frm]
    
    # IFFT, formula de Uuler
    
    for l in range(3):
        samples[l] = list(map(lambda x, y : x*np.exp(1j*y), samples[l], phases[l]))
        samples[l] = ifft(samples[l])
        
    # rehacer la señal
    # solo necesito rehacer samples[1], 
    out = np.zeros(1024)
    out[:512] = np.real(samples[0][512:]+samples[1][:512])
    out[512:] = np.real(samples[1][512:]+samples[2][:512])
            
    # y devolvemos una trama, hecha la ifft, rehacer la señal
        
    return out

signal_in = []
signal_out = np.zeros(1024) #[]
def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
   
    global signal_in, signal_out
    signal_in = np.append(signal_in, data)
    if len(signal_in) == 3072: # 2048:  #q .full():
        # hacemos el computo
        signal_out = noiseless(signal_in)
        # quitamos el primer chunk
        signal_in = signal_in[1024:]
        #signal_out = signal_out.astype(np.int16).tostring()
        signal_out = signal_out.astype(np.int16).tobytes()
    return (signal_out, pyaudio.paContinue)
    #return (data, pyaudio.paContinue)

p = pyaudio.PyAudio()
## open stream using callback
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
        time.sleep(12)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    

stream.stop_stream()
stream.close()

p.terminate()