# Librerías
from State import *
from Global import *

'''
    Class Name: Game
    Function: Almacenar los elementos estáticos del juego y llevar un registro de los estados generados.
'''
class Game:
    
    """
        Method Name: __init__
        Function: Constructor de la clase Game. 
    """
    def __init__(self, type_game : str ,str_json_game : str=None, state:State=None):
        self.name = type_game  # Modo de juego

        if str_json_game is not None:
            self.load_game(self.name,str_json_game) #Cargamos la configuracion inical del juego a traves de json
        else: # En caso de que quieras pasar un juego que no empieze en el estado inicial,
            self.size : int = DICC_GLOBAL_VARIABLES[type_game][0]
            self.scape : list = DICC_GLOBAL_VARIABLES[type_game][1]
            self.center : int = DICC_GLOBAL_VARIABLES[type_game][2]
            self.state = state # Estado del juego (no es necesario que sea el estado inicial)
        
        self.state_list : list = []
    

    """
        Method Name: load_state
        Function: Leer el json para cargar los datos del modo de juego seleccionado 
    """

    def load_game(self,game_name : str ,str_json : str) -> None:
     with open(str_json, 'r') as file:
            data = json.load(file)
            games = data["games"]
            for game_data in games:
                if game_data["name"] == game_name:
                    self.size : int  = game_data["size"]
                    self.scape : list = game_data["scape"]
                    self.center : int = game_data["center"]
                    self.state : State = State(self.name,"0000", game_data["white"], game_data["black"], game_data["king"], game_data["gamer"])


    def save_game_moves(self, filename,player_name, winner=None):
        # Recopilar la lista de estados visitados
        print("he entardo")
        moves_data = []

        # Recorrer la lista de estados visitados y añadirlos a la lista de movimientos, solo del primero cogemos el game id del resto empezamos directamente en la lista de white
        for state in self.state.visited_states:
            print(state)
            if state == self.state.visited_states[0]:
                moves_data.append({
                    "game_id": state.id,
                    "white": state.white,
                    "black": state.black,
                    "king": state.king,
                    "gamer": state.gamer
                })
            else:
                moves_data.append({
                    "white": state.white,
                    "black": state.black,
                    "king": state.king,
                    "gamer": state.gamer
                })

       
        # Obtener el color del jugador ganador si lo hay, para ello miramos el ultimo estado visitado
        if winner is not None:
            if winner == 0:
                winner_color = "black"
            elif winner == 1:
                winner_color = "white"
            else:
                winner_color = "empate"
        else:
            winner_color = "Nadie gana"

                # Cargar los datos del archivo existente si lo hay
        existing_data = {}
        try:
            with open(filename, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            pass

        # Agregar los movimientos al historial del jugador
        if player_name is not None:
            if player_name in existing_data:
                existing_data[player_name].append({
                    "moves": moves_data,
                    "winner": winner_color
                })
            else:
                existing_data[player_name] = [{
                    "moves": moves_data,
                    "winner": winner_color
                }]

        # Escribir el JSON en el archivo
        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)

    
    """
        Method Name: copy
        Function: realizar una copia del objeto Game
    """
    def copy(self):
        #new_game = Game(self.type_game, self.str_json_game, self.state.copy())
        new_game = Game(self.name, None, self.state.copy())
        return new_game
        
    """
        Method Name: __str__
        Function: devolver los valores del objeto en cadena
    """    
    def __str__(self) -> str:
        return f"Name: {self.name}\nSize: {self.size}\nScape: {self.scape}\nCenter: {self.center}\nState: \n{self.state}"
       
