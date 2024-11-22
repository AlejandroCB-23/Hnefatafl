# Librerías
import subprocess
import os
import Board
from Server import *
from Menu import *
from Player import *



# Ejecutar Server para validar usuario
server = Server()

if server.valid: # Usuario validado, se accede a la aplicación
    # Ejecutar Menú (encargado de comenzar partida, ver datos del usuario, modificar credenciales y salir)
    print("Acceso validado, bienvenid@  ", server.player.get_user()[0])
    while True: # Bucle infinito para que el usuario pueda realizar las acciones que desee
        menu = Menu(server.player)
        if menu.keep_running is False:
            break
        
    
else:
    print("<---------------------------------------  FIN DEL PROGRAMA --------------------------------------->")

print("<-----------------------------------APLICACIÓN CERRADA CON EXITO --------------------------------------->")

