# group delay
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import freqz, lfilter
import matplotlib.pyplot as plt

t = np.linspace(0,1,120)
#t = np.arange(120)
y = np.zeros(120)
print(t)
f0 = 5
s = np.cos(2*np.pi*f0*t)
a = 0.9
D = 20
for i in range(20,120):
    y[i] = -a*s[i] + s[i-D] + a*y[i-D]
# la filtro:
b = [0,1]
a = [1,0]
#filtrada = lfilter(b,a,s)
#filtrada = lfilter(b,a,y)
#w, h = freqz(b, a)
#group_delay = -diff(unwrap(angle(h))) / diff(w)
plt.plot(t,s,'g',t,y, 'r')
#plt.plot(t,s,'g',t,filtrada, 'r')
plt.show()