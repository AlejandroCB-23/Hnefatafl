import pygame
import json
from Game import Game
from State import State
from Menu import *
import time
import random
import tkinter as tk
from tkinter import messagebox
from MonteCarloBot import *
from RandomBot import *
from MinMaxBot import *
from Q_Bot import *
import matplotlib.pyplot as plt

# Definir algunos colores
CREMA = (255, 235, 205)
AZUL_CLARO = (173, 216, 230)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
ROJO = (236, 112, 99)

# Definir la dimensión de la pantalla y el tamaño del cuadrado
ANCHO_PANTALLA = 750
ALTO_PANTALLA = 525
TAMANO_CUADRADO = 75

# Variables para ejecutar bots
ITERATIONS = 10
DEPTH = 100

# elemento de persistencia donde guardamos los modos de juego
TYPE_GAME = "src/persistence/type_game.json"

class Cuadrado:
    def __init__(self, position : int,game_size : int):
        self.row = position // game_size # Se calcula la fila
        self.col = position % game_size # Se calcula la columna
        
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, CREMA, (self.col * TAMANO_CUADRADO, self.row * TAMANO_CUADRADO, TAMANO_CUADRADO, TAMANO_CUADRADO))
        pygame.draw.rect(pantalla, NEGRO, (self.col * TAMANO_CUADRADO, self.row * TAMANO_CUADRADO, TAMANO_CUADRADO, TAMANO_CUADRADO), 1)

    def dibujar_movimiento(self,pantalla):
        pygame.draw.rect(pantalla, ROJO, (self.col * TAMANO_CUADRADO, self.row * TAMANO_CUADRADO, TAMANO_CUADRADO, TAMANO_CUADRADO))
        pygame.draw.rect(pantalla, NEGRO, (self.col * TAMANO_CUADRADO, self.row * TAMANO_CUADRADO, TAMANO_CUADRADO, TAMANO_CUADRADO), 1)

    def dibujar_escape(self,pantalla):
        pygame.draw.line(pantalla, NEGRO, (self.col*TAMANO_CUADRADO, self.row*TAMANO_CUADRADO), ((self.col+1)*TAMANO_CUADRADO, (self.row+1)*TAMANO_CUADRADO), 3)
        pygame.draw.line(pantalla, NEGRO, (self.col*TAMANO_CUADRADO,(self.row+1)*TAMANO_CUADRADO), ((self.col+1)*TAMANO_CUADRADO,self.row*TAMANO_CUADRADO), 3)

    def dibujar_ficha(self,pantalla,color):
        pygame.draw.circle(pantalla,color,(TAMANO_CUADRADO*(self.col)+TAMANO_CUADRADO/2,TAMANO_CUADRADO*(self.row)+TAMANO_CUADRADO/2),30,0)
        


def dibujar_tablero(pantalla : pygame.Surface, game : Game, n_turn : int, games_remaining : int = None) -> None:
    
    size : int = game.size*game.size

    pantalla.fill(BLANCO)

    # Crear un objeto de fuente
    font = pygame.font.Font(None, 24)  # Fuente predeterminada con tamaño 36

    # Renderizar el primer texto en una superficie
    text_surface1 = font.render(f"TURNO: {n_turn}", True, (0, 0, 0))  # Texto, antialiasing, color
    text_surface2 = font.render(f"-- JUGADOR --", True, (0, 0, 0))  # Texto, antialiasing, color
    # Renderizar el segundo texto en una superficie
    if game.state.gamer == 0:
        text_surface3 = font.render(f"FICHAS NEGRAS", True, (0, 0, 0))  # Texto, antialiasing, color
    else:
        text_surface3 = font.render(f"FICHAS BLANCAS", True, (0, 0, 0))  # Texto, antialiasing, color

    # Renderizar el tercer texto en una superficie - dependiendo si games_remaining es None o no
    if games_remaining is not None:
        text_surface4 = font.render(f"-- JUEGOS RESTANTES --", True, (0, 0, 0))  # Texto, antialiasing, color
        text_surface5 = font.render(f"{games_remaining}", True, (0, 0, 0))  # Texto, antialiasing, color

        text_rect4 = text_surface4.get_rect()
        text_rect5 = text_surface5.get_rect()

        text_rect4.topright = (ANCHO_PANTALLA-20, 220)
        text_rect5.topright = (ANCHO_PANTALLA-110, 240)

        pantalla.blit(text_surface4, text_rect4)
        pantalla.blit(text_surface5, text_rect5)

        text_rect4.topleft = (ANCHO_PANTALLA - 40, 30)
        text_rect5.topleft = (ANCHO_PANTALLA - 40, 10)
    

    # Obtener el rectángulo de la superficie de texto
    text_rect1 = text_surface1.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_rect3 = text_surface3.get_rect()


    # Establecer la posición del primer texto en la esquina superior izquierda
    text_rect1.topright = (ANCHO_PANTALLA-69, 20)
    # Establecer la posición del segundo texto un poco más abajo
    text_rect2.topright = (ANCHO_PANTALLA-55, 60)
    # Establecer la posición del segundo texto un poco más abajo
    text_rect3.topright = (ANCHO_PANTALLA-42, 80)
    


    # Dibujar los textos en la superficie principal
    pantalla.blit(text_surface1, text_rect1)
    pantalla.blit(text_surface2, text_rect2)
    pantalla.blit(text_surface3, text_rect3)


    # Establecer la posición del primer texto en la esquina superior izquierda
    text_rect1.topleft = (ANCHO_PANTALLA - 40, 100)
    # Establecer la posición del segundo texto en la esquina superior derecha
    text_rect2.topright = (ANCHO_PANTALLA - 40, 40)
    # Dibujar los textos en la superficie principal
    text_rect3.topleft = (ANCHO_PANTALLA - 40, 60)


    for pos_tablero in range(size):
        #Primero dibujamos la figura del cuadrado (la casilla en cuestion)
        cuadrado = Cuadrado(pos_tablero,game.size)
        cuadrado.dibujar(pantalla)

        # Comprobamos que es una casilla de escape/centro
        if pos_tablero in game.scape or pos_tablero == game.center:
            cuadrado.dibujar_escape(pantalla)
        
        #Comprobamos si en pos_tablero debería ir una ficha negra
        if pos_tablero in game.state.black:
            cuadrado.dibujar_ficha(pantalla,NEGRO)

        #Comprobamos si en pos_tablero debería ir una ficha negra
        if pos_tablero in game.state.white:
            cuadrado.dibujar_ficha(pantalla,BLANCO)
        
        #Comprobamos si en pos_tablero debería ir la ficha del rey
        if pos_tablero == game.state.king:
            cuadrado.dibujar_ficha(pantalla,AZUL_CLARO)

        
            
def main(name, jugador):
    pygame.init()
    # Supongamos que la modalidad elegida por el usuario es la configuración basica (Brandubt)
    game = Game(name,str_json_game=TYPE_GAME)
    player_name = jugador
    print("\n",game.__str__())

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
    pygame.display.set_caption('Tablero de Ajedrez Vikingod')


    reloj = pygame.time.Clock()
    ejecutando : bool = True
    end_game : bool = False
    n_turn : int = 1

    dibujar_tablero(pantalla,game,n_turn) # Dibujamos el estado inicial

    while ejecutando and not(end_game): # loop inicial del juego
        movement_selected : bool = True
        
        pair_valid_moves = game.state.successor()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                    
            # si hacemos click, se tendria que mostrar los movimientos validos de la ficha seleccionada
            if event.type == pygame.MOUSEBUTTONDOWN:
                list_moves : list = []
                pos = pygame.mouse.get_pos()
                x = pos[0] // TAMANO_CUADRADO #columna
                y = pos[1] // TAMANO_CUADRADO #fila
                posicion_old = y * game.size + x
                                
                #Hay que comprobar si la posicion seleccionada es una ficha del jugador actual
                if game.state.gamer == 0 and posicion_old in game.state.black:
                    # Coloreamos las posiciones que se pueden mover dado la ficha seleccionada
                    for move in pair_valid_moves:
                        if move[0] == posicion_old:
                            list_moves.append(move[1])

                            cuadrado = Cuadrado(move[1],game.size)
                            cuadrado.dibujar_movimiento(pantalla)
                            print("Pintamos el movimiento")  
                    pygame.display.flip() # Actualiza la ventana con los movimientos validos

                    while movement_selected: # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                x = pos[0] // TAMANO_CUADRADO #columna
                                y = pos[1] // TAMANO_CUADRADO #fila
                                posicion_new = y * game.size + x

                                if posicion_new in list_moves:
                                    game.state = game.state.play((posicion_old,posicion_new))
                                    game.state.action_effect(posicion_new)
                                    game.state.gamer = (game.state.gamer + 1) % 2
                                    n_turn += 1
                                    
                                movement_selected = False

                elif game.state.gamer == 1 and posicion_old in game.state.white or posicion_old == game.state.king:
                    # Coloreamos las posiciones que se pueden mover dado la ficha seleccionada
                    for move in pair_valid_moves:
                        if move[0] == posicion_old:
                            list_moves.append(move[1])

                            cuadrado = Cuadrado(move[1],game.size)
                            cuadrado.dibujar_movimiento(pantalla)
                            print("Pintamos el movimiento")  
                    pygame.display.flip() # Actualiza la ventana con los movimientos validos

                    while movement_selected: # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                x = pos[0] // TAMANO_CUADRADO #columna
                                y = pos[1] // TAMANO_CUADRADO #fila
                                posicion_new = y * game.size + x

                                if posicion_new in list_moves:
                                    game.state = game.state.play((posicion_old,posicion_new))
                                    game.state.action_effect(posicion_new)
                                    game.state.gamer = (game.state.gamer + 1) % 2
                                    n_turn += 1
                                    
                                movement_selected = False

                end_game = juego_finalizado(game, player_name)

        dibujar_tablero(pantalla,game,n_turn)
        pygame.display.flip()  
        reloj.tick(60)

    # fin del juego
    show_popup(game.state.obtain_value(game.state.visited_states[-1]))
    # Procesar eventos de Pygame
    pygame.event.pump()
    pygame.quit()
    print("FIN DEL JUEGO\n")



def juego_finalizado(game : Game, player_name=None, v_results_iterations : list[int] = None, bot_attacker : Bot = None, bot_defender : Bot = None ) -> bool:
    if game.state.visited_states == []:
        return False
    
    value_state : int = game.state.obtain_value(game.state.visited_states[-1])
    print(f"El valor del estado es: {value_state}")
    fin : bool = False
    if game.state.king == -1 or value_state == -2 or value_state==1: # estados terminales
        fin = True
        #Miramos el ganador del juego
        if game.state.king == -1:
            print("CAPUTRA DEEL REEEY")
            if player_name is not None:
                game.save_game_moves("src/persistence/Registro.json", player_name, 0) #Ganan negras
            else:
                if isinstance(bot_attacker, MonteCarloBot):
                    game.save_game_moves("src/persistence/Registro.json", "MonteCarlo", 0) #Ganan negras
                elif isinstance(bot_attacker, RandomBot):
                    game.save_game_moves("src/persistence/Registro.json", "Random", 0)
                elif isinstance(bot_attacker, Q_Bot):
                    game.save_game_moves("src/persistence/Registro.json", "Q_Bot", 0)

                v_results_iterations[0] += 1
        else:
            if value_state == -2:
                if player_name is not None:
                    game.save_game_moves("src/persistence/Registro.json", player_name, 1) #Ganan blancas
                else:
                    if isinstance(bot_attacker, MonteCarloBot):
                        game.save_game_moves("src/persistence/Registro.json", "MonteCarlo", 1) #Ganan negras
                    elif isinstance(bot_attacker, RandomBot):
                        game.save_game_moves("src/persistence/Registro.json", "Random", 1)
                    elif isinstance(bot_attacker, Q_Bot):
                        game.save_game_moves("src/persistence/Registro.json", "Q_Bot", 1)
                    v_results_iterations[1] += 1
            if value_state == 1:
                if player_name is not None:
                    game.save_game_moves("src/persistence/Registro.json", player_name, 4) #Empate
                else:
                    if isinstance(bot_attacker, MonteCarloBot):
                        game.save_game_moves("src/persistence/Registro.json", "MonteCarlo", 4) #Ganan negras
                    elif isinstance(bot_attacker, RandomBot):
                        game.save_game_moves("src/persistence/Registro.json", "Random", 4)
                    elif isinstance(bot_attacker, Q_Bot):
                        game.save_game_moves("src/persistence/Registro.json", "Q_Bot", 4)
                    v_results_iterations[2] += 1

    return fin

def show_popup(last_value : int) -> None:
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    
    root.title("Fin del Juego")
    root.geometry("300x150")
    
    if last_value == -2:
        messagebox.showinfo("FIN DEL JUEGO","¡GANAN FICHAS BLANCAS!")
    elif last_value == 2:
        messagebox.showinfo("FIN DEL JUEGO","¡GANAN FICHAS NEGRAS!")
    elif last_value == 1:
        messagebox.showinfo("FIN DEL JUEGO","¡EMPATE!")

    root.update()
    root.destroy()

def show_popup_info(results : list[int], time_computed : float) -> None:
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    
    root.title("Fin del Juego")
    root.geometry("300x150")
    
    messagebox.showinfo("FIN DE LA SESIÓN",f"Numero de victorias atacantes: {results[0]}\nNumero de victorias defensores: {results[1]}\nNumero de empates: {results[2]}\nTiempo de ejecución: {round(time_computed,1)} segundos")

    root.update()
    root.destroy()

# Algoritmo que devuelve una posición aleatoria de un vector de n posiciones
def random_algorithms(n):
    random.seed(time.time())  # Utiliza la hora actual como semilla
    return random.randint(0, n - 1)


def monte_carlo_bot(name, jugador, bot): 
    pygame.init()
    # Supongamos que la modalidad elegida por el usuario es la configuración básica (Brandubt)
    game = Game(name, str_json_game=TYPE_GAME)
    player_name = jugador
    print("\n", game.__str__())

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption('Tablero de Ajedrez Vikingod')

    reloj = pygame.time.Clock()
    ejecutando = True
    end_game = False
    n_turn = 1

    dibujar_tablero(pantalla, game, n_turn)  # Dibujamos el estado inicial

    if bot == 1:
        while ejecutando and not end_game:  # loop inicial del juego
            movement_selected = True

            pair_valid_moves = game.state.successor()
            if game.state.gamer == 0:  # juega la persona, que jugará con las fichas negras
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ejecutando = False

                    # si hacemos click, se tendría que mostrar los movimientos válidos de la ficha seleccionada
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        list_moves = []
                        pos = pygame.mouse.get_pos()
                        x = pos[0] // TAMANO_CUADRADO  # columna
                        y = pos[1] // TAMANO_CUADRADO  # fila
                        posicion_old = y * game.size + x

                        # Hay que comprobar si la posición seleccionada es una ficha del jugador actual
                        if game.state.gamer == 0 and posicion_old in game.state.black:
                            # Coloreamos las posiciones que se pueden mover dada la ficha seleccionada
                            for move in pair_valid_moves:
                                if move[0] == posicion_old:
                                    list_moves.append(move[1])

                                    cuadrado = Cuadrado(move[1], game.size)
                                    cuadrado.dibujar_movimiento(pantalla)
                                    print("Pintamos el movimiento")
                            pygame.display.flip()  # Actualiza la ventana con los movimientos válidos

                            while movement_selected:  # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        pos = pygame.mouse.get_pos()
                                        x = pos[0] // TAMANO_CUADRADO  # columna
                                        y = pos[1] // TAMANO_CUADRADO  # fila
                                        posicion_new = y * game.size + x

                                        if posicion_new in list_moves:
                                            game.state = game.state.play((posicion_old, posicion_new))
                                            game.state.action_effect(posicion_new)
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1

                                            # Actualizar pantalla para mostrar el movimiento del jugador
                                            dibujar_tablero(pantalla, game, n_turn)
                                            pygame.display.flip()

                                            # Esperar 1 segundo antes de que el bot realice su movimiento
                                            time.sleep(1)
                                            

                                        movement_selected = False
            else: # Es el turno del bot, que jugaran con blancas
                montecarlo_bot_instance = MonteCarloBot(game)
                move = montecarlo_bot_instance.select_move()
                game.state = game.state.play(move)
                game.state.action_effect(move[1])
                game.state.gamer = (game.state.gamer + 1) % 2
                n_turn += 1

            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)

    else:
        # El bot juega primero
        montecarlo_bot_instance = MonteCarloBot(game)
        move = montecarlo_bot_instance.select_move()
        game.state = game.state.play(move)
        game.state.action_effect(move[1])
        game.state.gamer = (game.state.gamer + 1) % 2
        n_turn += 1

        while ejecutando and not end_game:
            movement_selected = True

            pair_valid_moves = game.state.successor()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecutando = False

                # si hacemos click, se tendría que mostrar los movimientos válidos de la ficha seleccionada
                if event.type == pygame.MOUSEBUTTONDOWN:
                    list_moves = []
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // TAMANO_CUADRADO
                    y = pos[1] // TAMANO_CUADRADO
                    posicion_old = y * game.size + x
                    
                    # Hay que comprobar si la posición seleccionada es una ficha del jugador actual
                    if game.state.gamer == 1 and posicion_old in game.state.white or posicion_old == game.state.king:
                        # Coloreamos las posiciones que se pueden mover dada la ficha seleccionada
                        for move in pair_valid_moves:
                            if move[0] == posicion_old:
                                list_moves.append(move[1])

                                cuadrado = Cuadrado(move[1], game.size)
                                cuadrado.dibujar_movimiento(pantalla)
                                print("Pintamos el movimiento")
                        pygame.display.flip()

                        while movement_selected:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    x = pos[0] // TAMANO_CUADRADO
                                    y = pos[1] // TAMANO_CUADRADO
                                    posicion_new = y * game.size + x

                                    if posicion_new in list_moves:
                                        game.state = game.state.play((posicion_old, posicion_new))
                                        game.state.action_effect(posicion_new)
                                        game.state.gamer = (game.state.gamer + 1) % 2
                                        n_turn += 1

                                        # Actualizar pantalla para mostrar el movimiento del jugador
                                        dibujar_tablero(pantalla, game, n_turn)
                                        pygame.display.flip()

                                        # Esperar 1 segundo antes de que el bot realice su movimiento
                                        time.sleep(1)
                                        
                                        # Verificar si es el turno del bot
                                        if game.state.gamer == bot:
                                            # El bot juega primero
                                            montecarlo_bot_instance = MonteCarloBot(game)
                                            move = montecarlo_bot_instance.select_move()
                                            game.state = game.state.play(move)
                                            game.state.action_effect(move[1])
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1

                                        movement_selected = False

                        
            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)

    # fin del juego
    show_popup(game.state.obtain_value(game.state.visited_states[-1]))
    # Procesar eventos de Pygame
    pygame.event.pump()
    pygame.quit()
    print("FIN DEL JUEGO\n")



def random_bot(name, jugador, bot):
    pygame.init()
    # Supongamos que la modalidad elegida por el usuario es la configuración básica (Brandubt)
    game = Game(name, str_json_game=TYPE_GAME)
    player_name = jugador
    print("\n", game.__str__())

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption('Tablero de Ajedrez Vikingod')

    reloj = pygame.time.Clock()
    ejecutando = True
    end_game = False
    n_turn = 1

    dibujar_tablero(pantalla, game, n_turn)  # Dibujamos el estado inicial

    if bot == 1:
        while ejecutando and not end_game:  # loop inicial del juego
            movement_selected = True

            pair_valid_moves = game.state.successor()
            if game.state.gamer == 0:  # juega la persona, que jugará con las fichas negras
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ejecutando = False

                    # si hacemos click, se tendría que mostrar los movimientos válidos de la ficha seleccionada
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        list_moves = []
                        pos = pygame.mouse.get_pos()
                        x = pos[0] // TAMANO_CUADRADO  # columna
                        y = pos[1] // TAMANO_CUADRADO  # fila
                        posicion_old = y * game.size + x

                        # Hay que comprobar si la posición seleccionada es una ficha del jugador actual
                        if game.state.gamer == 0 and posicion_old in game.state.black:
                            # Coloreamos las posiciones que se pueden mover dada la ficha seleccionada
                            for move in pair_valid_moves:
                                if move[0] == posicion_old:
                                    list_moves.append(move[1])

                                    cuadrado = Cuadrado(move[1], game.size)
                                    cuadrado.dibujar_movimiento(pantalla)
                                    print("Pintamos el movimiento")
                            pygame.display.flip()  # Actualiza la ventana con los movimientos válidos

                            while movement_selected:  # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        pos = pygame.mouse.get_pos()
                                        x = pos[0] // TAMANO_CUADRADO  # columna
                                        y = pos[1] // TAMANO_CUADRADO  # fila
                                        posicion_new = y * game.size + x

                                        if posicion_new in list_moves:
                                            game.state = game.state.play((posicion_old, posicion_new))
                                            game.state.action_effect(posicion_new)
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1

                                            # Actualizar pantalla para mostrar el movimiento del jugador
                                            dibujar_tablero(pantalla, game, n_turn)
                                            pygame.display.flip()

                                            # Esperar 1 segundo antes de que el bot realice su movimiento
                                            time.sleep(1)
                                            

                                        movement_selected = False
            else: # Es el turno del bot, que jugaran con blancas
                random_bot_instance = RandomBot(game)
                move = random_bot_instance.select_move()
                game.state = game.state.play(move)
                game.state.action_effect(move[1])
                game.state.gamer = (game.state.gamer + 1) % 2
                n_turn += 1

            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)

    else:
        # El bot juega primero
        random_bot_instance = RandomBot(game)
        move = random_bot_instance.select_move()
        game.state = game.state.play(move)
        game.state.action_effect(move[1])
        game.state.gamer = (game.state.gamer + 1) % 2
        n_turn += 1

        while ejecutando and not end_game:
            movement_selected = True

            pair_valid_moves = game.state.successor()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecutando = False

                # si hacemos click, se tendría que mostrar los movimientos válidos de la ficha seleccionada
                if event.type == pygame.MOUSEBUTTONDOWN:
                    list_moves = []
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // TAMANO_CUADRADO
                    y = pos[1] // TAMANO_CUADRADO
                    posicion_old = y * game.size + x
                    
                    # Hay que comprobar si la posición seleccionada es una ficha del jugador actual
                    if game.state.gamer == 1 and posicion_old in game.state.white or posicion_old == game.state.king:
                        # Coloreamos las posiciones que se pueden mover dada la ficha seleccionada
                        for move in pair_valid_moves:
                            if move[0] == posicion_old:
                                list_moves.append(move[1])

                                cuadrado = Cuadrado(move[1], game.size)
                                cuadrado.dibujar_movimiento(pantalla)
                                print("Pintamos el movimiento")
                        pygame.display.flip()

                        while movement_selected:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    x = pos[0] // TAMANO_CUADRADO
                                    y = pos[1] // TAMANO_CUADRADO
                                    posicion_new = y * game.size + x

                                    if posicion_new in list_moves:
                                        game.state = game.state.play((posicion_old, posicion_new))
                                        game.state.action_effect(posicion_new)
                                        game.state.gamer = (game.state.gamer + 1) % 2
                                        n_turn += 1

                                        # Actualizar pantalla para mostrar el movimiento del jugador
                                        dibujar_tablero(pantalla, game, n_turn)
                                        pygame.display.flip()

                                        # Esperar 1 segundo antes de que el bot realice su movimiento
                                        time.sleep(1)
                                        
                                        # Verificar si es el turno del bot
                                        if game.state.gamer == bot:
                                            random_bot_instance = RandomBot(game)
                                            move = random_bot_instance.select_move()
                                            game.state = game.state.play(move)
                                            game.state.action_effect(move[1])
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1

                                        movement_selected = False

                        
            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)

    # fin del juego
    show_popup(game.state.obtain_value(game.state.visited_states[-1]))
    # Procesar eventos de Pygame
    pygame.event.pump()
    pygame.quit()
    print("FIN DEL JUEGO\n")


def minmax_bot(name, jugador, bot):
    max_depth = 100
    minmax_bot_instance = MinMaxBot(max_depth)
    pygame.init()
    # Supongamos que la modalidad elegida por el usuario es la configuración básica (Brandubt)
    game = Game(name, str_json_game=TYPE_GAME)
    player_name = jugador
    print("\n", game.__str__())

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption('Tablero de Ajedrez Vikingod')

    reloj = pygame.time.Clock()
    ejecutando = True
    end_game = False
    n_turn = 1

    dibujar_tablero(pantalla, game, n_turn)  # Dibujamos el estado inicial
    pygame.display.flip()
    
    if bot == 0: # Si el bot es jugador de las fichas negras, el bot es el jugador 1 y el humano el jugador 2
        while ejecutando and not end_game:
            if game.state.gamer == 0: # juega el bot, que jugará con las fichas negras
                state_copy = game.state.copy()
                move = minmax_bot_instance.play(state_copy)[0]
                game.state = game.state.play(move)
                game.state.action_effect(move[1])
                game.state.gamer = (game.state.gamer + 1) % 2
                minmax_bot_instance.max_depth = max_depth # Reiniciamos la profundidad del algoritmo para las siguientes jugadas
                n_turn += 1
            else: # Le toca al humano, que jugará con las fichas blancas
                movement_selected : bool = True
                pair_valid_moves = game.state.successor()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ejecutando = False
                            
                    # si hacemos click, se tendria que mostrar los movimientos validos de la ficha seleccionada
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        list_moves : list = []
                        pos = pygame.mouse.get_pos()
                        x = pos[0] // TAMANO_CUADRADO #columna
                        y = pos[1] // TAMANO_CUADRADO #fila
                        posicion_old = y * game.size + x
                                        
                        if game.state.gamer == 1 and posicion_old in game.state.white or posicion_old == game.state.king:
                            # Coloreamos las posiciones que se pueden mover dado la ficha seleccionada
                            for move in pair_valid_moves:
                                if move[0] == posicion_old:
                                    list_moves.append(move[1])

                                    cuadrado = Cuadrado(move[1],game.size)
                                    cuadrado.dibujar_movimiento(pantalla)
                                    print("Pintamos el movimiento")  
                            pygame.display.flip() # Actualiza la ventana con los movimientos validos

                            while movement_selected: # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        pos = pygame.mouse.get_pos()
                                        x = pos[0] // TAMANO_CUADRADO #columna
                                        y = pos[1] // TAMANO_CUADRADO #fila
                                        posicion_new = y * game.size + x

                                        if posicion_new in list_moves:
                                            game.state = game.state.play((posicion_old,posicion_new))
                                            game.state.action_effect(posicion_new)
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1
                                            
                                        movement_selected = False

            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)
    else:
        while ejecutando and not end_game:
            if game.state.gamer == 1: # juega el bot, que jugará con las fichas blancas
                state_copy = game.state.copy()
                move = minmax_bot_instance.play(state_copy)[0]
                game.state = game.state.play(move)
                game.state.action_effect(move[1])
                game.state.gamer = (game.state.gamer + 1) % 2
                minmax_bot_instance.max_depth = max_depth # Reiniciamos la profundidad del algoritmo para las siguientes jugadas
                n_turn += 1
            else: # Le toca al humano, que jugará con las fichas blancas
                movement_selected : bool = True
                pair_valid_moves = game.state.successor()
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ejecutando = False
                            
                    # si hacemos click, se tendria que mostrar los movimientos validos de la ficha seleccionada
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        list_moves : list = []
                        pos = pygame.mouse.get_pos()
                        x = pos[0] // TAMANO_CUADRADO #columna
                        y = pos[1] // TAMANO_CUADRADO #fila
                        posicion_old = y * game.size + x
                                        
                        if game.state.gamer == 0 and posicion_old in game.state.black:
                            # Coloreamos las posiciones que se pueden mover dado la ficha seleccionada
                            for move in pair_valid_moves:
                                if move[0] == posicion_old:
                                    list_moves.append(move[1])

                                    cuadrado = Cuadrado(move[1],game.size)
                                    cuadrado.dibujar_movimiento(pantalla)
                                    print("Pintamos el movimiento")  
                            pygame.display.flip() # Actualiza la ventana con los movimientos validos

                            while movement_selected: # Bucle para que el programa no se cierre hasta que el usuario haga click en otra parte
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        pos = pygame.mouse.get_pos()
                                        x = pos[0] // TAMANO_CUADRADO #columna
                                        y = pos[1] // TAMANO_CUADRADO #fila
                                        posicion_new = y * game.size + x

                                        if posicion_new in list_moves:
                                            game.state = game.state.play((posicion_old,posicion_new))
                                            game.state.action_effect(posicion_new)
                                            game.state.gamer = (game.state.gamer + 1) % 2
                                            n_turn += 1
                                            
                                        movement_selected = False

            end_game = juego_finalizado(game, player_name)
            dibujar_tablero(pantalla, game, n_turn)
            pygame.display.flip()
            reloj.tick(60)

    # fin del juego
    show_popup(game.state.obtain_value(game.state.visited_states[-1]))
    # Procesar eventos de Pygame
    pygame.event.pump()
    pygame.quit()
    print("FIN DEL JUEGO\n")

def bot_vs_bot(game : Game, bot_attacker : Bot, bot_defender : Bot, n_iteraciones : int):    
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption('Tablero de Ajedrez Vikingod')

    reloj = pygame.time.Clock()
    ejecutando = True
    end_game = False
    n_turn = 1

    # Variable para almacenar las victorias de cada jugador y los empates en forma de vector
    # results[0] -> victorias del bot atacante (fichas negras)
    # results[1] -> victorias del bot defensor (fichas blancas)
    # results[2] -> empates
    results  = [0, 0, 0]

    last_2_states_black = []
    last_2_states_black.insert(0,None)
    last_2_states_black.insert(1,None)
    moves_black = []

    last_2_states_white = []
    last_2_states_white.insert(0,None)
    last_2_states_white.insert(1,None)
    moves_white = []

    reward_per_episode_black = []
    reward_per_episode_white = []

    # Variables auxiliares para la gestion de cuantas partidas se han jugador y cuantas quedan por jugar
    games_remaining = n_iteraciones
    time_start = time.time()
    while games_remaining > 0:
        reloj = pygame.time.Clock()
        ejecutando = True
        end_game = False
        n_turn = 1
        cumulative_reward_black : int = 0 # Recompensa acumulada por el bot atacante
        cumulative_reward_white : int = 0 # Recompensa acumulada por el bot atacante
        # Empezamos un nuevo juego, ayudado de una variable auxiliar
        game_aux = game.copy()
        dibujar_tablero(pantalla, game_aux, n_turn,games_remaining)  # Dibujamos el estado inicial
        pygame.display.flip()

        while ejecutando and not(end_game): # loop inicial del juego
            if game_aux.state.gamer == 0: # juega el bot atacante
                # Guardamos el estado anterior que habia jugador el bot atacante
                if len(game_aux.state.visited_states) > 2 and isinstance(bot_attacker, Q_Bot): # Si hay al menos dos estados en la lista
                    last_2_states_black[0] = game_aux.state.visited_states[-3]
                    last_2_states_black[1] = game_aux.state.visited_states[-1]
                    
                bot_attacker.game = game_aux.copy() # copiamos el estado del juego
                move = bot_attacker.select_move()
                moves_black.append(move)
                game_aux.state = game_aux.state.play(move)
                game_aux.state.action_effect(move[1])
                
                if isinstance(bot_attacker, Q_Bot) and n_turn >= 3:
                    reward = game_aux.state.reward(last_2_states_black[1])
                    cumulative_reward_black += reward
                    bot_attacker.learn(last_2_states_black[0],reward,last_2_states_black[1],moves_black[-2])

                
            else: # juega el bot defensor
                if len(game_aux.state.visited_states) > 3 and isinstance(bot_defender,Q_Bot): # Si hay al menos dos estados en la lista
                    last_2_states_white[0] = game_aux.state.visited_states[-3]
                    last_2_states_white[1] = game_aux.state.visited_states[-1]

                bot_defender.game = game_aux.copy() # copiamos el estado del juego
                move = bot_defender.select_move()
                moves_white.append(move)
                game_aux.state = game_aux.state.play(move)
                game_aux.state.action_effect(move[1])
                
                
                if isinstance(bot_defender, Q_Bot) and n_turn >= 4:
                    reward = game_aux.state.reward(last_2_states_white[1])
                    cumulative_reward_white += reward
                    bot_defender.learn(last_2_states_white[0],reward,last_2_states_white[1],moves_white[-2])

            n_turn += 1
            end_game = juego_finalizado(game_aux,v_results_iterations=results, bot_attacker=bot_attacker, bot_defender=bot_defender)
            # Cambiamos el turno
            game_aux.state.gamer = (game_aux.state.gamer + 1) % 2

            dibujar_tablero(pantalla,game_aux,n_turn,games_remaining)
            pygame.display.flip()  
            reloj.tick(60)

        games_remaining -= 1 #Actualizamos el numero de juegos restantes
        reward_per_episode_black.append(cumulative_reward_black)
        reward_per_episode_white.append(cumulative_reward_white)

    # fin del juego - mostraremos un informe de cuantas ha ganado negras y blancas
    time_end = time.time()

    # Si tenemos un bot Q, guardamos el modelo al finalizar una partida (un episodio de juego)
    if isinstance(bot_attacker, Q_Bot):
        bot_attacker.save_q_table()
        plt.plot(reward_per_episode_black)
        plt.show()
        print(f'LA MEDIA DE RECOMPENSAS POR EPISODIO ES: {np.mean(reward_per_episode_black)}')

    if isinstance(bot_defender, Q_Bot):
        bot_defender.save_q_table()
        plt.plot(reward_per_episode_white)
        plt.show()  
        print(f'LA MEDIA DE RECOMPENSAS POR EPISODIO ES: {np.mean(reward_per_episode_white)}')


    show_popup_info(results, time_end-time_start)
    pygame.event.pump()
    pygame.quit()

if __name__ == '__main__':
    main("Brandubt")
