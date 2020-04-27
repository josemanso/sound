# plot función
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

x = [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6,0.8,1]
y = np.zeros(len(x))
for i in range(len(x)):
    if 0 <=  abs(x[i]) and abs(x[i]) <= 1/3:
    #if 0 <=  x[i] and x[i] <= 1/3:
        y[i] = 2*x[i]
    elif 1/3<= abs(x[i]) and abs(x[i]) <=2/3:
    #elif 1/3<= x[i] and x[i] <=2/3:
        y[i] = x[i]/abs(x[i])*(3-(2-3*abs(x[i]))**2)/3
        #y[i] = (3-(2-3*x[i]**2))/3
    elif 2/3 <= abs(x[i]) <= 1:
        y[i] = x[i]/abs(x[i])*1#x[i] #1
        
print('y ', y)

        
plt.plot(x,y)
plt.title('Curva soft clip simétrico')
plt.ylabel('output')
plt.xlabel('input')

plt.grid()
            
plt.show()