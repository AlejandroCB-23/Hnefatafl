from Game import Game
from State import State

class Player:
    def __init__(self,name : str, password : str) -> None:
        self.name = name # Nombre del jugador (unico)
        self.password = password
    
    def __init__(self):
        self.name = ""
        self.password = ""

    def get_user(self) -> tuple:
        return self.name, self.password
    
    def mod_user(self, name : str, password : str) -> None:
        self.name = name
        self.password = password

    def __str__(self) -> str:
        return f"Name: {self.name}\nPassword: {self.password}"