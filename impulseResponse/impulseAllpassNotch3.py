# respuesta impulso "notch filter"
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from scipy.signal import iirnotch, freqz
import matplotlib.pyplot as plt

f1 = 300 # frecuencias de corte
f2 = 800
f3 = 1000
f4 = 4000
fs = 441000

r1 = 0.9
r2 = 0.98
r3 = 0.8
r4 = 0.9

theta1 = (1/fs)*f1*2*np.pi
theta2 = (1/fs)*f2*2*np.pi
theta3 = (1/fs)*f3*2*np.pi
theta4 = (1/fs)*f4*2*np.pi
    
AP1a1 = -2*r1*np.cos(theta1)
AP2a1 = -2*r2*np.cos(theta2)
AP3a1 = -2*r3*np.cos(theta3)
AP4a1 = -2*r4*np.cos(theta4)

AP1a2 = r1**2
AP2a2 = r2**2
AP3a2 = r3**2
AP4a2 = r4**2
ba1 = np.zeros(3)
ba2 = np.zeros(3)
ba3 = np.zeros(3)
ba4 = np.zeros(3)
aa1 = np.zeros(3)
aa2 = np.zeros(3)
aa3 = np.zeros(3)
aa4 = np.zeros(3)


ba1[0] = AP1a2  # a2
ba1[1] = AP1a1  # a1
ba1[2] = 1
aa1[0] = 1
aa1[1] = AP1a1
aa1[2] = AP1a2

ba2[0] = AP2a2  # a2
ba2[1] = AP2a1  # a1
ba2[2] = 1
aa2[0] = 1
aa2[1] = AP2a1
aa2[2] = AP2a2

ba3[0] = AP3a2  # a2
ba3[1] = AP3a1  # a1
ba3[2] = 1
aa3[0] = 1
aa3[1] = AP3a1
aa3[2] = AP3a2

ba4[0] = AP4a2  # a2
ba4[1] = AP4a1  # a1
ba4[2] = 1
aa4[0] = 1
aa4[1] = AP4a1
aa4[2] = AP4a2



Q = 2
bn1, an1 = iirnotch(f1/(fs/2), Q)
bn2, an2 = iirnotch(f2/(fs/2), Q)
bn3, an3 = iirnotch(f3/(fs/2), Q)
bn4, an4 = iirnotch(f4/(fs/2), Q)



w, h = freqz(np.concatenate((bn1,bn2,bn3,bn4)), np.concatenate((an1,an2,an3,an4)))
freq = w*fs/(2*np.pi)
w1, h1 = freqz(np.concatenate((ba1,ba2,ba3,ba4), axis=0), np.concatenate((aa1,aa2,aa3,aa4)))


#plot
fig, ax = plt.subplots(2, 1, figsize=(8, 6))
#plt.title('Respuesta Notch') 
#ax[1].plot(freq, np.unwrap(np.angle(h))*180/np.pi)
ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')
ax[0].set_xlabel('iirnotch')

ax[1].plot(freq, 20*np.log10(abs(h1)), color='blue')
ax[1].set_xlabel('allpas iirnotch')

plt.grid()
plt.show()
