# Librerías
import random
import time
from Game import Game
from Bot import Bot  


"""
    Class name: MonteCarloBot
    Function: bot que selecciona la "mejor" jugada para un jugador x en un estado y aplicando el algoritmo de Monte Carlo.
"""
class MonteCarloBot(Bot):

    # Definir variables iniciales de la clase
    def __init__(self, game: Game):
        self.root_game = game # Clase Game con el estado inicial (root)
        self.children = self.root_game.state.successor() # Movimientos posibles para el estado raíz (nodos hijo al expandir el árbol)
        self.results = [0]*len(self.children) # Seguimiento del número de victorias y derrotas durante el algoritmo
        self.simulation_no = 500 # Número de simulaciones (cuanto mayor sea el valor, más costoso es el algoritmo, pero más exacto)


    """
        Method name: select_move
        Function: función que devuelve el nodo correspondiente al mejor movimiento posible
    """
    def select_move(self):
        for i in range(self.simulation_no):
            # Se crea una nueva copia de la clase game con el estado raíz
            root_game_copy = self.root_game.copy()

            # Seleccionamos el primer movimiento posible aleatoriamente
            n = self.select_action(len(self.children)-1)

            # Simulamos expandiendo el árbol aleatoriamente una partida completa hasta un nodo hoja y obtenemos el resultado de la partida
            result = self.expand(root_game_copy, n)

            # Actualizamos los resultados
            self.results[n] = self.results[n] + result
        
        best_action = self.results.index(max(self.results))
        print(self.results)
        print("valor max:",self.results[best_action] )
        print(best_action)
        return self.children[best_action]



    # Devuelve aleatoriamente una acción de los movimientos posibles
    def select_action(self, length):
        return  random.randint(0, length)


    # Simulamos la partida
    def expand(self, root: Game, v):
        # Simulamos el primer movimiento seleccionado
        move = root.state.successor()[v]
        root.state = root.state.play(move)
        root.state.action_effect(move[1])
        root.state.gamer = (root.state.gamer + 1) % 2

        # Se simula hasta que lleguemos a un nodo terminal (fin de partida)
        while root.state.obtain_value(root.state) == 0:
            # Se expande el árbol, se simula un turno aleatoriamente
            legal_moves = root.state.successor()
            n = self.select_action(len(legal_moves)-1)
            move = legal_moves[n]
            root.state = root.state.play(move)
            root.state.action_effect(move[1])
            root.state.gamer = (root.state.gamer + 1) % 2

        return root.state.valoration(self.root_game.state.gamer)