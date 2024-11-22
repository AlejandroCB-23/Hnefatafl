import time
from Game import Game
from Bot import Bot  
import random
class RandomBot(Bot):
    def __init__(self, game: Game):
        self.game = game

    def select_move(self):
        legal_moves = self.game.state.successor()  
        if legal_moves:
            # Generar un índice aleatorio basado en el tiempo actual
            random.seed(time.time())
            index = random.randint(0, len(legal_moves) - 1)
            
            return legal_moves[index]  # Devolver un movimiento aleatorio
        

