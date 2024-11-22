# Librerías
import json
import bisect
import hashlib
from Global import *


'''
    Class Name: State
    Function: Representa el estado del tablero en un turno del juego y es capaz de generar todos los movimientos válidos de cada ficha en el tablero.
'''
class State:
    
    """
        Method Name: __init__
        Function: Constructor de la clase State. 
    """
    def __init__(self,type_game : str,id:str = None, white:list=None, black:list=None, king:int=None, gamer:int=None, str_json=None):
        self.type_game  = type_game # Modo de juego
        
        if str_json is not None: 
            self.load_state(str_json) # en el caso de que se pase un archivo json
        else: 
            self.white = white
            self.black = black
            self.king = king
            self.gamer = gamer
            

            

        self.id = self.get_id() # Identificador del estado
        # Formato de la lista de succesores: (nombre_accion, estado_resultante, valor_accion)
        self.st_successors : list = []
        # inicializamos la lista de visitados con el estado inicial
        # los demas estados se añadiran en la funcion play
        self.visited_states = [self]
       

    """
        Method Name: get_id
        Function: devuelve el identificador del estado, que corresponderia a un identificador hash md5
    """
    def get_id(self) -> str:
        str_list_white : str = ""
        str_list_black : str = ""

        for elemento in self.white:
            str_list_white = str_list_white + str(elemento)

        for elemento in self.black:
            str_list_black = str_list_black + str(elemento)

        str_id = str_list_white + str_list_black + str(self.king) + str(self.gamer)

        return hashlib.md5(str_id.encode()).hexdigest()      
    """
        Method Name: copy
        Function: Crea una copia de si mismo y la devuelve.
    """
    def copy(self):
        new_State = State(self.type_game,self.id, self.white[:], self.black[:], self.king, self.gamer)
        new_State.visited_states = self.visited_states[:]
        return new_State
    
    """
        Method Name: load_state
        Function: Carga el estado desde un archivo json 
    """
    def load_state(self,str_json):
     with open(str_json, 'r') as file:
            data = json.load(file) # Cargamos el archivo json de un estado en concreto y rescatamos sus características
            self.white = data["white"]
            self.black = data["black"]
            self.king = data["king"]
            self.gamer = data["gamer"]
            self.id = self.get_id() # Identificador del estado


    """
        Method Name: successor
        Function: Generar todos los sucesores posibles (los movimientos legales de cada una de las fichas que pueden mover en el turno).
    """
    def successor(self) -> list:
        pair_valid_moves : list = []
        
        if(self.gamer == 0): # 0 == atacante (1º turno siempre atacante)
            for i in self.black:
                n : int = i
                # 1º while (eje x positivo)
                self.valid_values_x_pos(pair_valid_moves, n, False)
                # 2º while (eje x negativo)
                self.valid_values_x_neg(pair_valid_moves, n, False)
                # 3º while (eje y positivo)
                self.valid_values_y_pos(pair_valid_moves, n, False)
                # 4º while (eje y negativo)
                self.valid_values_y_neg(pair_valid_moves, n, False)


        else: # 1 == defensor 
            for i in self.white:
                n : int = i                
                # 1º while (eje x positivo)
                self.valid_values_x_pos(pair_valid_moves, n, False)
                # 2º while (eje x negativo)
                self.valid_values_x_neg(pair_valid_moves, n, False)
                # 3º while (eje y positivo)
                self.valid_values_y_pos(pair_valid_moves, n, False)
                # 4º while (eje y negativo)
                self.valid_values_y_neg(pair_valid_moves, n, False)

            # Se comprueba el rey
             # 1º while (eje x positivo)
            self.valid_values_x_pos(pair_valid_moves, self.king, True)
            # 2º while (eje x negativo)
            self.valid_values_x_neg(pair_valid_moves, self.king, True)
            # 3º while (eje y positivo)
            self.valid_values_y_pos(pair_valid_moves, self.king, True)
            # 4º while (eje y negativo)
            self.valid_values_y_neg(pair_valid_moves, self.king, True)

        ordered_moves : list = []
        for move in pair_valid_moves:
            ordered_moves = self.insert_sorted(ordered_moves, move[0], move[1])
        
        return ordered_moves


    """
        Method Name: valid_values_x_pos
        Function: Devuelve los valores legales de la posición n en el eje x positivo.
    """            
    def valid_values_x_pos(self, pair_valid_moves : list, n : int, is_king : bool) -> None:
        go : bool = True
        old_n : int = n
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0]

        while go:
            # Primero calculamos si estamos dentro del tablero
            if (n % size) == size - 1: # Estamos en el límite del eje x positivo (salimos del bucle)
                go = False
            else:
                # Actualizamos n_new
                n = n + 1
                                
                # Comprobamos si la nueva casilla es válida
                valid, go = self.is_valid(n, is_king)
                if valid:
                    pair_valid_moves.append((old_n, n))



    """
        Method Name: valid_values_x_neg
        Function: Devuelve los valores legales de la posición n en el eje x negativo.
    """   
    def valid_values_x_neg(self, pair_valid_moves : list, n : int, is_king : bool) -> None:
        go : bool = True
        old_n : int = n
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0]

        while go:
            # Primero calculamos si estamos dentro del tablero
            if (n % size) == 0: # Estamos en el límite del eje x negativo (salimos del bucle)
                go = False
            else:
                # Actualizamos n_new
                n = n - 1
                                
                # Comprobamos si la nueva casilla es válida
                valid, go = self.is_valid(n, is_king)
                if valid:
                    pair_valid_moves.append((old_n, n))


    """
        Method Name: valid_values_y_pos
        Function: Devuelve los valores legales de la posición n en el eje y positivo.
    """   
    def valid_values_y_pos(self, pair_valid_moves : list, n : int, is_king : bool) -> None:
        go : bool = True
        old_n : int = n
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0]

        while go:
            # Primero calculamos si estamos dentro del tablero
            if (n // size) == 0: # Estamos en el límite del eje y positivo (salimos del bucle)
                go = False
            else:
                # Actualizamos n_new
                n = n - size
                
                # Comprobamos si la nueva casilla es válida
                valid, go = self.is_valid(n, is_king)
                if valid:
                    pair_valid_moves.append((old_n, n))



    """
        Method Name: valid_values_y_neg
        Function: Devuelve los valores legales de la posición n en el eje y negativo.
    """   
    # Devuelve los valores legales de la posición n en el eje y negativo
    def valid_values_y_neg(self, pair_valid_moves : list, n : int, is_king : bool) -> None:
        go : bool = True
        old_n : int = n
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0]

        while go:
            # Primero calculamos si estamos dentro del tablero
            if (n // size) == size - 1: # Estamos en el límite del eje y negativo (salimos del bucle)
                go = False
            else:
                # Actualizamos n_new
                n = n + size

                # Comprobamos si la nueva casilla es válida
                valid, go = self.is_valid(n, is_king)
                if valid:
                    pair_valid_moves.append((old_n, n))

    """
        Method Name: is_valid
        Function: Método para comprobar si una casilla es válida (se tiene cuenta si eres rey o no para las casillas especiales).
    """   
    def is_valid(self, n : int, is_king : bool) -> tuple:
        # Se comprueba si hay una ficha en la posición y se devuelve True = válida  False = no válida
        valid : bool = True
        can_jump : bool = True
        if self.is_empty(n):
            # Si es rey no hace falta comprobar las casillas especiales
            if(not is_king):
                if(self.is_special(n)):
                    valid = False
        else:
            valid = False
            can_jump = False

        return valid, can_jump # can_jump determina si seguir o no, ya que con casillas especiales se puede saltar (una ficha no). Y valid define si se añade o no a la lista de estados válidos
        

    """
        Method Name: is_empty
        Function: Comprueba si en la posición n hay alguna ficha.
    """   
    def is_empty(self, n : int) -> bool:
        is_empty : bool = True
        # Se comprueban las fichas negras
        if n in self.black:
            is_empty = False
        # Se comrpueba las fichas blancas y el rey
        else:
            if n in self.white:
                is_empty = False
            if self.king == n:
                is_empty = False
        # Se devuelve el valor para saber si está vacía o no
        return is_empty
    
    """
        Method Name: is_special
        Function: Devuelve valor booleano para determinar si la casilla n es especial o no (scape or center).
    """ 
    def is_special(self, n : int) -> bool:
        scape : list = DICC_GLOBAL_VARIABLES[self.type_game][1]
        center : list = DICC_GLOBAL_VARIABLES[self.type_game][2]

        if n in scape or n == center:
            return True
        else:
            return False
        
    """
        Method Name: insert_sorted
        Function: Inserta valores (old_n, n) en pair_valid_moves de manera ordenada.
    """ 
    def insert_sorted(self, pair_valid_moves : list, old_n : int, n : int) -> list:
        index_to_insert : int = 0
        for move in pair_valid_moves:
            # Comparamos las coordenadas (old_n, n) con cada par en pair_valid_moves
            if move[0] > old_n or (move[0] == old_n and move[1] > n):
                break
            index_to_insert += 1
        pair_valid_moves.insert(index_to_insert, (old_n, n))
        return pair_valid_moves
    
    """
        Method Name: obtain_value
        Function: devuelve la valoración de un estado.
    """
    def obtain_value(self, state : 'State') -> int:
        #Si el rey es distinto de -1, es que no ha sido capturado
        scape = DICC_GLOBAL_VARIABLES[self.type_game][1]
        if state.king != -1:
            if state.king in scape: 
                return -2
        else:
            return 2 # Ganan las fichas negras
        
        if len(state.black) == 0:
            return -2
          
        #Comprobamos que no sea empate, es decir que se hayan repetido los id de los estados 3 veces

        if self.check_for_cycle():
            return 1  # Devolver 1 para indicar un empate

       
        return 0
    
    """
        Method Name: check_for_cycle
        Function: Comprueba si se ha repetido 3 veces un estado en la lista de visitados.
    """

    def check_for_cycle(self) -> bool:
        #Tenemos que comprobar que una combinacion de estados se hayan repetido 3 veces en la lista de visitados mirando su id
        #Si se repite 3 veces, es un empate
        #Si no, se devuelve False

            all_states = self.visited_states
            #Imprimo los estados visitados los id de los estados visitados

            n = len(all_states)

            if n < 6:
                return False
            
            id_list = [state.id for state in all_states] #Lista de id`s estados visitados

            max_sequence_length = n // 3 #Maxima longitud de la secuencia que se puede repetir 3 veces

            for sequence_length in range(2, max_sequence_length + 1): #Comprobamos cadenas desde longitud 2 hasta la longitud maxima
                for i in range(n - sequence_length * 2 + 1):  #Nos aseguramos de que no nos salgamos de la lista de id`s ya que una vez elegido el tamaño de la secuencia, solo podremos comprobar hasta el final de la lista - 2 veces el tamaño de la secuencia
                    sequence = id_list[i:i + sequence_length]  #Cogemos una secuencia de longitud sequence_length
                    repeated_sequence = True

                    for j in range(1, 3): #Comprobamos si la secuencia se repite 3 veces
                        if sequence != id_list[i + sequence_length * j:i + sequence_length * (j + 1)]: #Si no se repite, cambiamos el valor de repeated_sequence a False y salimos del bucle
                            repeated_sequence = False
                            break

                    if repeated_sequence:
                        return True

            return False
    

    """
        Method Name: play
        Function: dado un movimiento, actualiza el estado del tablero ya que esta funcion devuelve un estado nuevo
        despues de evaluarse el movimiento.

        @param mov: movimiento a realizar, es una tupla con la posición inicial y final del movimiento (pos,new_pos)

        La utilidad de este método es crear S', la evaluacion vendrá en un paso posterior en la clase game.
    """

    def play(self,mov : tuple) -> 'State': # Devuelve un nuevo estado
        new_state : 'State' = self.copy()
        print("COPIA DEL ESTADO: ",new_state.__str__())
        pos : int = mov[0]
        new_pos : int = mov[1]

        #Dependiendo del jugador que sea, se actualiza una lista de fichas o otra
        #Ten en cuenta de que a la hora de eliminar la antigua posicion por la nueva, la lista se actualiza y se mantiene en orden.

        if self.gamer == 1:
            if pos != new_state.king:
                new_state.white.remove(pos)
                bisect.insort(new_state.white,new_pos)
            else:
                new_state.king = new_pos
        else:
            new_state.black.remove(pos)
            bisect.insort(new_state.black,new_pos)
            print("NEW Black: ",new_state.black)

        # Una vez actualizado la lista, se debería evaluar los efectos de dicha jugada (captura de fichas, cambio de turno, etc)
        # codigo para implementar la evaluacion de los efectos action_effect(new_pos) y que queda reflejado en el nuevo estado.
        # self.action_effect(new_state, pos, new_pos)
            
        new_state.id = new_state.get_id() # Actualizamos el id del nuevo estado
        print(f"Nuevo estado: {new_state.id}")
        new_state.visited_states.append(new_state) # Añadimos el nuevo estado a la lista de visitados

        return new_state


    """
        Method Name: obtain_succesors_state
        Function: devuelve la lista de succesores del estado actual
        Representaremos los sucesores como una lista de tuplas (nombre_accion, estado_resultante, valoracion)
    """
    def obtain_succesors_state(self) -> list:
        successors : list = []
        pair_valid_moves : list = self.successor() # Generamos los sucesores del estado actual
       
        for move in pair_valid_moves:
            new_state = self.play(move) # Generamos el estado resultante para cada movimiento valido
            value = self.obtain_value(new_state) # Obtenemos la valoracion de cada estado resultante
            successors.append((move, new_state, value))
            
        return successors
        
    """ 
        Method Name: action_effect
        Function: evaluar los efectos de una jugada.
        @param new_pos: nueva posicion de la ficha, ¿que efectos va a tener mover la ficha en esa posicion?
        ¿Qué devuelve?
        0 -> blancos ganan
        1 -> negros ganan
        2 -> se sigue jugando (se actualiza el estado nuevo)
    """

    def action_effect(self, new_pos : int) -> None:
        # Se debe comprobar las fichas atrapadas, si el rey alcanza una casilla especial de las esquinas (gana defensores) o si atrapan al rey (gana atacantes). 
        
        # Variables
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0] # Tamaño del tablero
        center : int = DICC_GLOBAL_VARIABLES[self.type_game][2] #Casilla central
        scape : list = DICC_GLOBAL_VARIABLES[self.type_game][1]
        i : int = new_pos // size
        j : int = new_pos % size
        

        # ¿Qué jugador ha movido?
        if self.gamer == 1: # Defensores (blancos)
            
            # Se comprueba si se ha atrapado alguna negra
            # X positivo
            if j < size - 2: # Si no lo cumple, no puede atrapar nadie en el eje positivo x
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.black:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (i == n//size) and n-new_pos == 1 and ((n+1 in self.white or n+1 == self.king) or (n+1 == center and self.king != center) or (n+1 in scape)):
                        # Se elimina la ficha negra (atrapada)
                        self.black.remove(n)
                        print(f"FICHA NEGRA ATRAPADA:{n}\n")
                    
                    
            # X negativo
            if j > 1 : # Si no lo cumple, no puede atrapar nadie en el eje negativo x
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.black:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (i == n//size) and n-new_pos == -1 and ((n-1 in self.white or n-1 == self.king) or (n-1 == center and self.king != center) or (n-1 in scape)):
                        # Se elimina la ficha negra (atrapada)
                        self.black.remove(n)
                        print(f"FICHA NEGRA ATRAPADA:{n}\n")
                    
      
            # Y positivo
            if i > 1 : # Si no lo cumple, no puede atrapar nadie en el eje positivo y
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.black:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (j == n%size) and new_pos-n == size and ((n-size in self.white or n-size == self.king) or (n-size == center and self.king != center) or (n-size in scape)):
                        # Se elimina la ficha negra (atrapada)
                        self.black.remove(n)
                        print(f"FICHA NEGRA ATRAPADA:{n}\n")
                                

            # Y negativo
            if i < size - 2 : # Si no lo cumple, no puede atrapar nadie en el eje negativo y
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.black:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (j == n%size) and n-new_pos == size and ((n+size in self.white or n+size == self.king) or (n+size == center and self.king != center) or (n+size in scape)):
                        # Se elimina la ficha negra (atrapada)
                        self.black.remove(n)
                        print(f"FICHA NEGRA ATRAPADA:{n}\n")

        else: # Atacantes (negros)

            # Se comprueba si se ha atrapado alguna blanca
            # X positivo
            print("X POSITIVO NEGRO")
            if j < size - 2: # Si no lo cumple, no puede atrapar nadie en el eje positivo x
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.white:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (i == n//size) and n-new_pos == 1 and (n+1 in self.black or (n+1 == center and self.king != center) or (n+1 in scape)):
                        # Se elimina la ficha negra (atrapada)
                        self.white.remove(n)
                        print(f"FICHA BLANCA ATRAPADA:{n}\n")
                    
                    
            # X negativo
            print("X NEGATIVO NEGRO")
            if j > 1 : # Si no lo cumple, no puede atrapar nadie en el eje negativo x
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.white:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (i == n//size) and n-new_pos == -1 and (n-1 in self.black or (n-1 == center and self.king != center) or (n-1 in scape)):
                        # Se elimina la ficha blanca (atrapada)
                        self.white.remove(n)
                        print(f"FICHA BLANCA ATRAPADA:{n}\n")
                    
      
            # Y positivo
            print("Y POSITIVO NEGRO")
            if i > 1 : # Si no lo cumple, no puede atrapar nadie en el eje positivo y
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.white:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (j == n%size) and new_pos-n == size and (n-size in self.black or (n-size == center and self.king != center) or (n-size in scape)):
                        # Se elimina la ficha blanca (atrapada)
                        self.white.remove(n)
                        print(f"FICHA BLANCA ATRAPADA:{n}\n")
                                

            # Y negativo
            print("Y NEGATIVO NEGRO")
            if i < size - 2 : # Si no lo cumple, no puede atrapar nadie en el eje negativo y
                # Se recorre todas las fichas negras para comprobar si atrapa alguna
                for n in self.white:
                    # Captura normal con 2 fichas o captura con una ficha y una casilla central/escape
                    if (j == n%size) and n-new_pos == size and (n+size in self.black or (n+size == center and self.king != center) or (n+size in scape)):
                        # Se elimina la ficha blanca (atrapada)
                        self.white.remove(n)
                        print(f"FICHA BLANCA ATRAPADA:{n}\n")


            # Se comprueba si atrapa rey  
            i_king : int = self.king // size
            j_king : int = self.king % size
            king_capture : bool = True
            
            if not (i_king  == 0 or  j_king == 0 or i_king == size-1 or j_king == size-1 ):
                potential_attackers = [self.king + 1, self.king - 1, self.king - size, self.king + size]
                
                # Si la ficha movida está entre los posibles atacantes (posibilidad de rey atrapado)
                if(new_pos in potential_attackers):
                    potential_attackers.remove(new_pos)
                    if center in potential_attackers: # Caso especial de captura con 3 fichas y el rey (ficha central)
                        potential_attackers.remove(center)

                    # para que el rey sea atrapado, todos los posibles atacantes deben estan rodeando al rey
                    for t in potential_attackers: # Se recorre los atacantes restantes para ver si hay una ficha negra
                        if not t in self.black: # Si no hay una ficha negra en rodeando el rey el rey no está atrapado
                            king_capture = False
                            break
                            
                    if king_capture:
                        self.king = -1 # El rey ha sido atrapado
                        print("REY ATRAPADO")
                                
    """
        Method Name: profit //modificar para mejorar la exactitud del algoritmo
        Function: devolver el valor de un estado para cierto jugador side
        0 -> Atacantes
        1 -> Defensores
    """
    def profit(self, side) -> float:
        if side == 0: # Atacantes
            return len(self.black)
        else: # Defensores
            return len(self.white) + 1 


    def valoration(self, side): # side indica el lado del jugador que nos interesa side = 0 (atacantes) side = 1 (defensores)
        # Empate = 0
        if self.check_for_cycle() or self.obtain_value(self) == 1:
            return 0
        
        # Ganan atacantes (negras)
        if self.obtain_value(self) == 2:
            if side == 0:
                return 1
            else:
                return -1
        # Ganan defensores (blancas)
        if self.obtain_value(self) == -2:
            if side == 0:
                return -1
            else:
                return 1

    def reward(self, state : 'State') -> float:
        reward : int = 0
        if state.gamer == 0: # Atacantes
            if state.king == -1:
                reward = 100
            else:
                reward = state.get_balance_pieces()*3 - state.get_distance_king_to_scape()*2 + state.get_distance_to_king()*4 + state.get_value_pieces_eaten()*1.5
        else: # Defensores
            scape = DICC_GLOBAL_VARIABLES[self.type_game][1]
            if state.king in scape:
                 reward -100
            else:
                reward = state.get_balance_pieces()*3 - state.get_distance_king_to_scape()*4 - state.get_distance_to_king()*2.5 - state.get_value_pieces_eaten()*1.5
            
        return reward

    def get_balance_pieces(self) -> float:
        return len(self.black) - (len(self.white)+1)*1.6
    
    def get_balance_movements(self) -> float:
        aux_state = self.copy()
        if self.gamer == 0:
            moves_black : int = len(aux_state.successor())
            aux_state.gamer = 1
            moves_white : int = len(aux_state.successor())
        else:
            moves_white : int = len(aux_state.successor())
            aux_state.gamer = 0
            moves_black : int = len(aux_state.successor())
        
        return moves_black - moves_white
    
    '''
        Metodo para obtener la distancia del rey a la salida
        Para eso, calcularemos la distancia heuclideana entre el rey y la salida mas cercana, a menos distancia, mejor
    '''
    def get_distance_king_to_scape(self) -> float:
        # Obtenemos la posicion del rey, tanto en filas como en columnas
        size = DICC_GLOBAL_VARIABLES[self.type_game][0]
        scape = DICC_GLOBAL_VARIABLES[self.type_game][1]

        row_king = self.king // size
        col_king = self.king % size
        min_distance = float('inf') # Variable para guardar la distancia minima

        # Calculamos la distancia euclideana entre el rey y la salida mas cercana
        for scape_pos in scape:
            row_scape = scape_pos // size
            col_scape = scape_pos % size

            distance = ((row_king - row_scape)**2 + (col_king - col_scape)**2)**0.5
            if distance < min_distance:
                min_distance = distance

        return 10/min_distance
    
    def get_distance_to_king(self) -> float:
        # Obtenemos la posicion del rey, tanto en filas como en columnas
        size = DICC_GLOBAL_VARIABLES[self.type_game][0]
        
        row_king = self.king // size
        col_king = self.king % size
        distance : float = 0.0

        # Calculamos la distancia euclideana entre el rey y todas las fichas negras
        for black_pos in self.black:
            row_black = black_pos // size
            col_black = black_pos % size

            if row_king == row_black or col_king == col_black: # bonificacion por estar en la misma fila o columna (Bonificacion de 5)
                distance += 1/(((row_king - row_black)**2 + (col_king - col_black)**2)**0.5+1) + 10
            else:
                distance += 1/(((row_king - row_black)**2 + (col_king - col_black)**2)**0.5+1) 

        mean_distance = distance/len(self.black)

        return 30/mean_distance
    
    '''
        Metodo para evaluar si el estado dado, dependiendo si son blancas o negras, se podria comer en ese turno a alguna ficha
    '''
    def get_value_pieces_eaten(self) -> int:
        # Se debe comprobar las fichas atrapadas, si el rey alcanza una casilla especial de las esquinas (gana defensores) o si atrapan al rey (gana atacantes). 
        
        # Variables
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0] # Tamaño del tablero
        i : int
        j : int
        valoracion : int = 0 # Valoracion de la funcion
        valid_moves = self.successor()
        bonus_points : int = 10

        if self.gamer == 0: # Si el bot es jugador de las fichas negras
            # Sacamos los movimientos validos de las fichas negras
            # Recorremos cada movimiento valido y miramos si se puede comer alguna ficha de las blancas
            for white_pos in self.white:
                for move in valid_moves:
                    # Captura en eje X a la izquierda
                    if move[1] == (white_pos-1) and (white_pos+1) in self.black:
                        valoracion += bonus_points

                    # Captura en eje X a la derecha
                    if move[1] == (white_pos+1) and (white_pos-1) in self.black:
                        valoracion += bonus_points

                    # Captura en eje Y hacia arriba
                    if move[1] == (white_pos-size) and (white_pos+size) in self.black:
                        valoracion += bonus_points

                    # Captura en eje Y hacia abajo
                    if move[1] == (white_pos+size) and (white_pos-size) in self.black:
                        valoracion += bonus_points
        else: # Si el bot es jugador de las fichas blancas
            for black_pos in self.black:
                for move in valid_moves:
                    # Captura en eje X a la izquierda
                    if move[1] == (black_pos-1) and (black_pos+1) in self.white:
                        valoracion += bonus_points

                    # Captura en eje X a la derecha
                    if move[1] == (black_pos+1) and (black_pos-1) in self.white:
                        valoracion += bonus_points

                    # Captura en eje Y hacia arriba
                    if move[1] == (black_pos-size) and (black_pos+size) in self.white:
                        valoracion += bonus_points

                    # Captura en eje Y hacia abajo
                    if move[1] == (black_pos+size) and (black_pos-size) in self.white:
                        valoracion += bonus_points

        return valoracion

    '''
        Metodo para evaluar si el estado dado, dependiendo si son blancas o negras, el bot podria ser comido en ese turno algunas de sus fichas
        la logica es la misma que en el metodo get_value_pieces_eaten, pero en este caso se evalua si el bot podria ser comido
        es decir, hace la funcion inversa que get_value_pieces_eaten
    ''' 
    def get_pen_eaten(self) -> int:
                # Variables
        size : int = DICC_GLOBAL_VARIABLES[self.type_game][0] # Tamaño del tablero
        i : int
        j : int
        valoracion : int = 0 # Valoracion de la funcion
        valid_moves = self.successor()
        bonus_points : int = 10
        state_aux = self.copy()
        state_aux.gamer = (state_aux.gamer + 1) % 2 # Cambiamos el turno para evaluar si el bot podria ser comido

        if state_aux.gamer == 0: # Si el bot es jugador de las fichas negras
            # Sacamos los movimientos validos de las fichas negras
            # Recorremos cada movimiento valido y miramos si se puede comer alguna ficha de las blancas
            for white_pos in self.white:
                for move in valid_moves:
                    # Captura en eje X a la izquierda
                    if move[1] == (white_pos-1) and (white_pos+1) in self.black:
                        valoracion += bonus_points

                    # Captura en eje X a la derecha
                    if move[1] == (white_pos+1) and (white_pos-1) in self.black:
                        valoracion += bonus_points

                    # Captura en eje Y hacia arriba
                    if move[1] == (white_pos-size) and (white_pos+size) in self.black:
                        valoracion += bonus_points

                    # Captura en eje Y hacia abajo
                    if move[1] == (white_pos+size) and (white_pos-size) in self.black:
                        valoracion += bonus_points
        else: # Si el bot es jugador de las fichas blancas
            for black_pos in self.black:
                for move in valid_moves:
                    # Captura en eje X a la izquierda
                    if move[1] == (black_pos-1) and (black_pos+1) in self.white:
                        valoracion += bonus_points

                    # Captura en eje X a la derecha
                    if move[1] == (black_pos+1) and (black_pos-1) in self.white:
                        valoracion += bonus_points

                    # Captura en eje Y hacia arriba
                    if move[1] == (black_pos-size) and (black_pos+size) in self.white:
                        valoracion += bonus_points

                    # Captura en eje Y hacia abajo
                    if move[1] == (black_pos+size) and (black_pos-size) in self.white:
                        valoracion += bonus_points

        return valoracion
    
    """
        Method Name: __str__
        Function: devolver los valores del objeto en cadena.
    """
    def __str__(self) -> str: 
        return f"Game ID: {self.id}\nWhite: {self.white}\nBlack: {self.black}\nKing: {self.king}\nGamer: {self.gamer}"

    