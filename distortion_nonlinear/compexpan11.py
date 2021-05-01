# Compresor expansor
# Compressor Expander
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


def comprexpander(x, ratio, th_compress, th_expan):
    # x data input
    # ratio  ratio conpressor 1/ratio, expander ratio
    # th  threshold
    AT = 0.9
    RT = 0.097
    th_c = 10**(th_compress/20)* 32769 # 2¹⁵
    th_e = 10**(th_expan/20) * 32769
    print( 'the' ,th_e)
    cn = np.zeros(len(x))
    gain = np.ones(len(x))
    gain_c = np.ones(len(x))
    gain_e = np.ones(len(x))
    out = np.zeros(len(x))
    out[0] = x[0]
    cn[0] = abs(x[0]) #
    for i in range(1,len(x)):
        #cn[i] = 0.9 * cn[i-1] + 0.1 * abs(x[i])
        cn[i] = abs(x[i])
        
        if abs(x[i]) > th_c:
            #compressor(i, x, ratio, th_c, d, gain)
            if cn[i] > cn[i-1]:
                #cn[i] = (1-AT)*cn[i-1] + AT * cn[i]
                #cn[i] = cn[i-1]
                cn[i] = cn[i]
                #cn[i] = (1-RT)*cn[i-1]
            else:
                #cn[i] = (1-RT)*cn[i-1]
                #cn[i] = cn[i]
                cn[i] = cn[i-1]
                #cn[i] = (1-AT)*cn[i-1] + AT * cn[i]
                
            #gain[i] = (cn[i] / th_c)**(1/ratio - 1)
            gain[i] = (th_c/cn[i])**(1-1/ratio)
            gain_c[i] = gain[i]
            # sino gain = 1   
        #if (abs(x[i]) < th_e) and (abs(x[i]) > 0.0001):
        
        elif abs(x[i]) < th_e:
            if (abs(x[i]) > 10):
            #if (abs(x[i]) > 0.00001):
                gain[i] =1/ (cn[i] /th_e)**(ratio -1)
                #gain[i] = (cn[i] /th_e)**(ratio -1)
                #gain[i] = (th_e / cn[i])**(ratio -1)
                gain_e[i] = gain[i]
            else:
                gain[i] = 0
                gain_e[i] = gain[i]
            # expander excpto el ruido
            #if abs(x[i]) > 0.0001:
                # mayor que sonido muybajo ó ruido
                # solo si es mayo se expande
            #if cn[i] <= th_e :
                #gain[i] = (th_e /cn[i])**(ratio - 1)
            #gain[i] = (cn[i] /th_e)**(ratio -1)
            #gain_e[i] = gain[i]
            #and (abs(x[i]) > 0.001):
            #expander(i, x, ratio, th_e, d, gain)
        
        else:
            gain[i] =1
        out[i] = x[i]*gain[i]
    #plt.plot(gain[])
    #plt.show()
    return out, gain, gain_c, gain_e
    
# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "fish.wav"
        
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
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)

# fuera de la curva con ganancia 1

#datan = data / 32768  # 2¹⁶ /2
th_comp= -10 # dB
th_exp = -60 # dB
#attack = 0.1
#release = 0.94
CR = 4 # ratio  log10(4 ) = 0,6
#CR = 0.6
#y = compexpander(datan, attack, release, CR, thComp, thExp)
y, g, gc, ge = comprexpander(data, CR, th_comp, th_exp)

#threshold=0.01)

#y = y * 32768
# write wav file
try:
    wavfile.write('/home/josemo/python/wavfiles/comprexpander1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)    
#plot
time = np.arange(len(data))/fs
plt.figure(1)
#plt.subplot(211)
plt.plot(time, y, 'r--', time, data,'g--')
plt.xlabel('Señal original verde, señal comprimida /espandida, rojo')
#plt.subplot(212)
plt.figure(2)
# máx alrededor de 3.6, antes

plt.plot(time,data, 'g--',time,y, 'r--')
plt.xlabel('Señal original verde, señal comprimida /espandida, rojo')

plt.figure(3)
plt.plot(time,g)
plt.figure(4)
plt.plot(time,gc)
plt.xlabel('compresión')
plt.figure(5)
plt.plot(time,ge)
plt.xlabel(' expansión ')

plt.grid()
plt.show()