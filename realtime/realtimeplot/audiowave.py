try:
    import pyaudio
    import numpy as np
    import time
    from tkinter import TclError
    import matplotlib.pyplot as plt

except ImportError:
    raise ImportError('Faltan móduos externos que instalar')



CHUNK = 2**12 # 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
#frames = []
# iniciar stream de audio
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)


#definición de la figura (matplotlib)
fig, ax = plt.subplots(figsize=(14,6))

x = np.arange(0, 2*CHUNK, 2)
# límites de los ejes
ax.set_title('Audio wave')
ax.set_xlabel('Amplitud')
ax.set_ylabel('samples')
ax.set_ylim(-10000,10000)
ax.set_xlim(0,CHUNK)#make sure our x axis matched our chunk size
line, = ax.plot(x, np.random.rand(CHUNK))

print('stream started')

# for measuring frame rate
frames_count = 0
start_time = time.time()

# hecho nuestri gráfico, podemos empezar a plotear nuestra señal
while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, np.int16)
    line.set_ydata(data)
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)
    except TclError:
        # calculate average frame rate
        frame_rate = frames_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break

plt.show()
    

