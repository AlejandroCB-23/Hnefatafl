from Game import Game
from State import State
from Variable import *
import time

'''
    Implementacion del algoritmo minimax con poda alfa-beta
'''

class MinMaxBot:
    def __init__(self, max_depth : int) -> None:
        self.max_depth = max_depth


    '''
        Metodo play para elegir la mejor jugada utilizando el algoritmo minimax con poda alfa-beta
    '''
    def play(self,state : State) -> tuple:
        if state.gamer == 0: # Si el bot es jugador de las fichas negras
            return self.minimax_max(state, float('-inf'), float('inf'),self.max_depth)
        else: # Si el bot es jugador de las fichas blancas
            return self.minimax_min(state, float('-inf'), float('inf'),self.max_depth)
    
    def minimax_max(self, state : State, alpha : int, beta : int,depth:int,mov : tuple = None) -> tuple:
        if self.is_terminal(state) or depth == 0:
            return (mov,self.evaluate(state))
        else:
            max_value = float('-inf')
            best_move = None
            
            valid_moves = state.successor() # Obtenemos los movimientos validos en forma de lista

            # Recorremos cada jugada valida, creando su estado y valorando el estado
            for move in valid_moves:
                new_state = state.play(move) # Obtenemos el nuevo estado
                new_state.action_effect(move[1]) # Aplicamos el efecto de la jugada, dependiendo de la posicion final de la ficha movida
                new_state.gamer = (new_state.gamer + 1) % 2
                aux_value = max(max_value,self.minimax_min(new_state, alpha, beta,depth-1,move)[1]) # Obtenemos el valor del estado

                if aux_value >= beta: # Poda beta
                    return (move, aux_value) # Realiza la poda, porque nos pasamos de beta
                else:
                    alpha = max(alpha, aux_value)
                    
                if aux_value > max_value: # Nuevo mejor movimiento
                    max_value = aux_value
                    best_move = move

            return (best_move, max_value)
        

        
    def minimax_min(self, state : State, alpha : int, beta : int, depth : int,mov : tuple = None) -> tuple:
        if self.is_terminal(state) or depth == 0:
            return (mov,self.evaluate(state))
        else:
            min_value = float('inf')
            best_move = None
            
            valid_moves = state.successor() # Obtenemos los movimientos validos en forma de lista

            # Recorremos cada jugada valida, creando su estado y valorando el estado
            for move in valid_moves:
                new_state = state.play(move) # Obtenemos el nuevo estado
                new_state.action_effect(move[1]) # Aplicamos el efecto de la jugada, dependiendo de la posicion final de la ficha movida
                new_state.gamer = (new_state.gamer + 1) % 2
                aux_value = min(min_value,self.minimax_max(new_state, alpha, beta,depth-1,move)[1]) # Obtenemos el valor del estado

                if aux_value <= alpha: # Poda alfa
                    return (move, aux_value) # Realiza la poda, porque nos estamos por debajo de alfa
                else:
                    beta = min(beta, aux_value)

                if aux_value < min_value: # Nuevo mejor movimiento
                    min_value = aux_value
                    best_move = move

            return (best_move, min_value)

    def is_terminal(self, state : State) -> bool:
        #Si el rey es distinto de -1, es que no ha sido capturado
        scape = DICC_GLOBAL_VARIABLES[state.type_game][1]
        
        if state.king != -1:
            if state.king in scape: 
                return True # Ganan las fichas blancas
        else:
            return True # Ganan las fichas negras
        
        if len(state.black) == 0:
            return True # Ganan las fichas blancas
          
        #Comproobamos que no sea empate, es decir que se hayan repetido los id de los estados 3 veces
        if state.check_for_cycle(): 
            return True  # caso de empate
       
        return False
    
    def evaluate(self, state : State) -> int:
        # Funcion de evaluacion de un estado, respecto a las fichas negras
        # La funcion de evaluacion es la diferencia de fichas blancas y negras
        scape = DICC_GLOBAL_VARIABLES[state.type_game][1]
        
        if state.king != -1:
            if state.king in scape: 
                return -2
        else:
            return 2 # Ganan las fichas negras
        
        if len(state.black) == 0: 
            return -2 # Ganan las fichas blancas
          
        #Comproobamos que no sea empate, es decir que se hayan repetido los id de los estados 3 veces
        if state.check_for_cycle():
            return 1  # caso de empate
       
        return 0



    


        

    
    
        
        