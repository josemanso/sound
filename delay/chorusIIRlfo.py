# Chorus effects con IIR
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt


# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "yooh.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
        
    
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/josemo/python/wavfiles/"+file_input):
    filename ="/home/josemo/python/wavfiles/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()
    
#
# read wave file
fs, data = wavfile.read(filename)

# Chorus multivoz

# retraso voz 1 m = 0.02 * fs = 882, 0.015 = 662, delay1 = 800, delay2= 660
# LFO frec rate at 0.1 - 5 Hz LFO; (rate) delay; Fd = 0.1 y fd2 = 0.3 ( randon a mano)
# ganancias a 0.98 y 0.97
# entre 40 y 60 ms y alrededor de 0.25 Hz
delay = 800 # samples
delay1 = 700
b = np.zeros(delay)
#b[-1] = 1
b[0] = 1
a = np.zeros(delay)
a[0] = 1
a[-1] = -0.60  # ganancia
n = np.arange(delay)
b1 = np.zeros(delay1)
b1[0] =1
#b1[-1] = 1

a1= np.zeros(delay1)
a1[0] = 1
a1[-1] = -0.70  # ganancia
n1 = np.arange(delay1)

delay2 = 900
a2= np.zeros(delay2)
b2 = np.zeros(delay2)
b2[0] = 1
a2[0] = 1
a2[-1] = -0.65  # ganancia
n2 = np.arange(delay1)
# LFO


lfo_ref = np.sin(2*np.pi*0.01/fs)
lfo_ref1 = np.sin(2*np.pi*0.03/fs)

lfo_ref2 = np.sin(2*np.pi*0.02/fs)


denum = a + lfo_ref
denum1 = a1 + lfo_ref1

denum2 = a2 + lfo_ref2

data_filt = lfilter(b,denum, data)
data_filt1 = lfilter(b1, denum1, data)
data_filt2 = lfilter(b2, denum2, data)

data_all =(data_filt + data_filt1 + data_filt2)/4

wavfile.write('/home/josemo/python/wavfiles/chorus.wav', 
              fs, data_all.astype(np.int16))
fs1, data1 = wavfile.read('/home/josemo/python/wavfiles/chorus.wav')
time = np.arange(len(data))/fs
plt.plot(time, data1, 'r--',time, data,'g--')
plt.title('Chorus')
plt.xlabel('Original verde, Coro rojo')
plt.show()

