try:
    import pyaudio
    import numpy as np
    from matplotlib import use
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
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

# hecho nuestri gráfico, podemos empezar a plotear nuestra señal
while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, np.int16)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

plt.show()
    

