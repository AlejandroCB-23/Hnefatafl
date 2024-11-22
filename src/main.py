# Librerías
import json
import pygame
import sys
from pygame.locals import *
from Game import *
from Variable import * # Para las variables globales


''' Evitamos que se muestre la interfaz
# Se inicia pygame
pygame.init() 

# Se crea la pantalla o display

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) 

# Se muestra el menú principal
run = True
while run: 
    action = main_menu(display)

    if(action == 1):
        select_dashboard_menu(display) # Si la acción seleccionada es la 1
'''


def main() -> None:
    pruebas_creacion_juegos_y_estados()
    pruebas_funcion_succesora()
    prueba_juego1()


def pruebas_creacion_juegos_y_estados() -> None:
    # Primero pedimos por consola que diga que modo de juego quiere:
    # Inicializamos el juego de Brandubt a traves de cargar el json
    type_game : str = "Brandubt"
    new_game : Game = Game(type_game,"src/persistence/type_game.json") # Cargamos el juego de Brandubt del archivo global de estados iniciales

    print(new_game.__str__()) # Ya tenemos cargado el Game y el State inicial según el modo de juego que se seleccione
    pair_valid_moves : list = new_game.state.successor()

    # Prueba de cargar solo un estado en concreto (a traves de su json)
    generic_state : State = State(type_game,str_json="src/persistence/state.json")
    print("\nState: ",generic_state.__str__())

    # Prueba de cargar el archivo global de estados iniciales
    variables_brandubt : tuple = DICC_GLOBAL_VARIABLES[type_game]
    print("\nVariables Brandubt: ",variables_brandubt)

    # Prueba de crear un juego nuevo que empiece en un estado concreto
    generic_game : Game = Game(type_game,state=generic_state)
    print("\nGeneric Game: ",generic_game.__str__())

    # Abrimos el archivo en modo escritura
    with open("Pair_Valid_Moves", 'w') as archivo:
        # Escribimos cada valor de la lista en una línea separada
        for valor in pair_valid_moves:
            archivo.write(str(valor) + '\n')


def pruebas_funcion_succesora() -> None:
    #Creamos el juego de Brandubt
    type_game : str = "Brandubt"
    # Cargamos el juego de Brandubt del archivo global de estados iniciales
    game : Game = Game(type_game,str_json_game="src/persistence/type_game.json")
    # Generamos los sucesores del estado actual
    pair_valid_moves : list = game.state.successor()
    # Mostramos los sucesores
    print("Estos son los movimientos validos para las fichas negras...\n",pair_valid_moves)
    # Mostramos la funcion successor
    game.state.st_successors = game.state.obtain_succesors_state()
    print("\nFuncion sucesora\n",game.state.st_successors)
    
'''
    metodo donde se simula una version reducida de un juego completo, para ver si el intercambio de movimientos
    se hace correctamente
'''
def prueba_juego1() -> None:
    # Creamos el estado generico
    type_game : str = "Brandubt"
    seguir : bool = True
    cont_turns : int = 1
    state : State = State(type_game,str_json="src/persistence/generic_state.json")

    # Creamos el juego de Brandubt
    game : Game = Game(type_game,state=state)
    print("Estado inicial: ",game.state.__str__())

    # bucle principal del juego
    while seguir and game.state.king != -1:
        invalid_play : bool = True
        print(f"\nTurno {cont_turns}")
        if game.state.gamer == 0:
            print(f"turno del jugador con las fichas negras")
        else:
            print(f"turno del jugador con las fichas blancas")

        # Mostramos el estado del tablero
        print(game.state.__str__())

        while invalid_play:
            # Mostramos los movimientos validos del estado actual
            print("------------[MOVIMIENTOS VALIDOS]------------")
            pair_valid_moves : list = game.state.successor()
            index : int = 0
            for moves in pair_valid_moves:
                print(f"[{index}] {moves}\n")
                index += 1
            # Pedimos el movimiento al usuario
            print("Introduce el movimiento que quieres hacer (Selecciona el indice del movimiento que quieres hacer)")
            move = input()
            # Comprobamos si el movimiento es valido
            if move.isdigit() and int(move) < len(pair_valid_moves):
                invalid_play = False
            else:
                print("Movimiento invalido, vuelve a intentarlo")

        pos : tuple = pair_valid_moves[int(move)]
        new_pos : int = pos[1]   

        # Realizamos el movimiento
        game.state = game.state.play(pair_valid_moves[int(move)]) # Realizamos el movimiento, actualizando el estado del juego

        game.state.action_effect(new_pos) # Actualizamos el estado del juego
        game.state.gamer = game.state.gamer = (game.state.gamer + 1) % 2 # Formula general sin condicionales para cambiar de jugador

        print("FIN TURNO\n")
        cont_turns += 1

    print("FIN DEL JUEGO\n")

if __name__ == "__main__":
    main()

'''
for event in pygame.event.get(): #
    if event.type == QUIT:
        pygame.quit # Se cierra la pantalla
        sys.exit # Se cierra la aplicación
pygame.display.flip() # Actualiza la ventana
'''
