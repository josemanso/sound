# compresor expansor tiempo real 
import numpy as np
import pyaudio
import time

RATE = 44100

th_comp= -5 # dB
th_exp = -70 # dB
CR  = 4


def compressor(ind, xc, R, th, d, gain):
    rcomp = 1/R # ratio compressor
    d0 = th # threshold
    
    if abs(xc[ind]) >= abs(xc[ind-1]):
        d[ind] = d[ind-1] + abs(xc[ind])
    else:
        d[ind] = d[ind-1]
    # ganacia para comprimir
    if d[ind] >= d0:
        gain[ind] = (d[ind]/d0)**(rcomp-1)

def expander(ind, xe, Ra, thresh, d, gain):
    rexp = Ra+2
    d0 = thresh
    
    if abs(xe[ind-1] < 0.0001):
        # ruido
        gain[ind-1]=0
    else:
        if abs(xe[ind]<= abs(xe[ind-1])):
            d[ind] = d[ind-1] +abs(xe[ind])
            #d[ind] = d[ind-1]
        else:
            d[ind] = d[ind-1]
            #d[ind] = d[ind-1] +abs(xe[ind])
        #gain
        if d[ind] <= d0:
            if d[ind] < 0.0001:
                d[ind] = 0.0001
            #gain[ind] = (d[ind]/d0)**(rexp-1)
            gain[ind] = (d0/d[ind])**(rexp-1)
            
def comprexpander(x, ratio, th_compress, th_expan):
    # x data input
    # ratio  ratio conpressor 1/ratio, expander ratio
    # th  threshold
    
    th_c = 10**(th_compress/20)
    th_e = 10**(th_expan/20)
    d = np.zeros(len(x))
    gain = np.ones(len(x))
    out = np.zeros(len(x))
    out[0] = x[0]
    
    for i in range(1,len(x)):
        if abs(x[i]) > th_c:
            compressor(i, x, ratio, th_c, d, gain)
            
        elif (abs(x[i]) < th_e) and (abs(x[i]) > 0.0001):
            expander(i, x, ratio, th_e, d, gain)
        else:
            gain[i] =1
        out[i] = x[i]*gain[i]
    return out
    


pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #data1 = data.copy()
    # hacemos el computo
    #data1 = data1/ norm # valores entre 1 y -1
    datan = data / 32768  # 2¹⁶ /2
    y = comprexpander(datan, CR, th_comp, th_exp)

    y = y * 32768

    
    sample = y.astype(np.int16).tostring()
    #return (in_data, pyaudio.paContinue)
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

        
