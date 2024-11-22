'''
Programa de prueba para ver si el algoritmo minimax funciona correctamente, sin necesidad de ejecutar el juego completo y sin interfaz
'''

from Game import Game
from State import State
from MinMaxBot import MinMaxBot
import time

def main():
    type_game = "Brandubt"
    # Creamos un estado inicial generico, no es necesario que sea un juego real
    generic_state = State(type_game,str_json="src/persistence/generic_state.json") # Creamos un estado generico
    print(f'\nEstado inicial: {generic_state.__str__()}\n')

    # Creamos el bot, otorgandole una profundidad maxima de busqueda
    bot = MinMaxBot(8)
    inicio = time.time()
    # Obtenemos la mejor jugada a partir del estado generico
    best_move = bot.play(generic_state)
    fin = time.time()

    print(f'\nTiempo de ejecucion: {fin-inicio} segundos\n')
    print(f'\nLa mejor jugada es: {best_move[0].__str__()},\n con un valor de: {best_move[1]}\n')

if __name__ == "__main__":
    main() # Ejecutamos el programa principal
    
    