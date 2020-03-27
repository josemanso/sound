#reprodución
import sys
import os
from playsound import playsound

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = 'grabacion.wav'
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(e)

# excepcion de fichero

if os.path.isfile("/home/josemo/python/wavfiles/"+file_input):
    filename ="/home/josemo/python/wavfiles/"+file_input
    
    print('file exit')
    
else:
    print('File not exit')
    exit()

    
playsound(filename)