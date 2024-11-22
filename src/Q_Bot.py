from Bot import Bot
import numpy as np
from Game import Game
from State import State
import json

class Q_Bot(Bot):
    def __init__(self, game:Game, player : int,alpha: float = 0.1, gamma: float = 1, epsilon: float = 0.05):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = dict()
        self.player = player
        self.game = game
        # Q-tabla dependiendo del jugador (si es negras o blancas)
        if player == 0:
            #Recuperamos la q-table de las fichas negras de neustra persistencia
            with open('src/persistence/q-table_black.json', 'r') as file:
                self.q_table = json.load(file)
        else:
            #Recuperamos la q-table de las fichas blancas de neustra persistencia
            with open('src/persistence/q-table_white.json', 'r') as file:
                self.q_table = json.load(file) 

    '''
        Method Name: select_random_move
        Function: selecciona un movimiento aleatorio o un movimiento que maximiza el valor Q
        según lo que salga en el sorteo
    '''
    def select_move(self):
        if np.random.uniform(0,1) < self.epsilon:
            return self.select_random_move()
        else:
            if self.game.state.id not in self.q_table:
                return self.select_random_move()
            else:
                q_values_of_state = self.q_table[self.game.state.id]
                max_value = max(q_values_of_state.values())
                action = np.random.choice([a for a, value in q_values_of_state.items() if value == max_value])

        # Devolvemos el movimiento seleccionado en forma de tupla
        return eval(action)

    def select_random_move(self):
        legal_moves = self.game.state.successor()
        if legal_moves:
            return legal_moves[np.random.randint(0, len(legal_moves))]
        else:
            return None # No devolver nada si no hay movimientos legales
        
    def learn(self, old_state : State, reward : float, new_state : State, action : tuple):
        '''Actualiza la q-tabla con la nueva información obtenida de la partida'''
        if old_state.id not in self.q_table:
            # Creamos la nueva entrada de nuestra q-tabla con los movimientos validos y un valor de 0
            valid_moves = old_state.successor()
            self.q_table[old_state.id] = {str(move): 0 for move in valid_moves}
        
        if new_state.id not in self.q_table:
            # Creamos la nueva entrada de nuestra q-tabla con los movimientos validos y un valor de 0
            valid_moves = new_state.successor()
            self.q_table[new_state.id] = {str(move): 0 for move in valid_moves}

        q_values_of_state = self.q_table[new_state.id]
        max_q_value_in_new_state = max(q_values_of_state.values())
        current_q_value = self.q_table[old_state.id][str(action)]
            
        self.q_table[old_state.id][str(action)] = current_q_value + self.alpha * (reward + self.gamma * max_q_value_in_new_state - current_q_value)

    def save_q_table(self):
        '''Guarda la q-tabla en un archivo json para persistir los datos'''
        if self.player == 0:
            with open('src/persistence/q-table_black.json', 'w') as file:
                json.dump(self.q_table, file)
        else:
            with open('src/persistence/q-table_white.json', 'w') as file:
                json.dump(self.q_table, file)
            
        