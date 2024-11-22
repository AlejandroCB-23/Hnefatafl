# Librerías
import json

'''
    Module Name: Stadistics
    Function: Módulo para gestionar las estadísticas de los distintos bots.
'''

datos_random = "src/persistence/statistics/random_statistics.json"
datos_montecarlo = "src/persistence/statistics/monte_carlo_statistics.json"
datos_qlearning ="src/persistence/statistics/qlearning_statistics.json"


# Método para modificar estadísticas del bot random (valores de resultado --> 1 = ganado  0 = empate -1 = perder)
def mod_stadistics_random(tipo_bot, color, resultado):
    # Cargar el JSON
    with open(datos_random, 'r') as file:
        data = json.load(file)
    
    data[tipo_bot][color]["partidas_jugadas"] += 1

    if resultado == 1:
        data[tipo_bot][color]["partidas_ganadas"] += 1
    elif resultado == -1:
        data[tipo_bot][color]["partidas_perdidas"] += 1
    else:
        data[tipo_bot][color]["partidas_empatadas"] += 1

    # Guardar los datos actualizados en el JSON
    with open(datos_random, 'w') as file:
        json.dump(data, file, indent=2)


# Método para modificar estadísticas del bot montecarlo
def mod_stadistics_montecarlo(tipo_bot, color, resultado):
    # Cargar el JSON
    with open(datos_montecarlo, 'r') as file:
        data = json.load(file)
    
    data[tipo_bot][color]["partidas_jugadas"] += 1
    
    if resultado == 1:
        data[tipo_bot][color]["partidas_ganadas"] += 1
    elif resultado == -1:
        data[tipo_bot][color]["partidas_perdidas"] += 1
    else:
        data[tipo_bot][color]["partidas_empatadas"] += 1

    # Guardar los datos actualizados en el JSON
    with open(datos_montecarlo, 'w') as file:
        json.dump(data, file, indent=2)




# Método para modificar estadísticas del bot Q-learning
def mod_stadistics_qlearning(tipo_bot, color, resultado):
    # Cargar el JSON
    with open(datos_qlearning, 'r') as file:
        data = json.load(file)
    
    data[tipo_bot][color]["partidas_jugadas"] += 1
    
    if resultado == 1:
        data[tipo_bot][color]["partidas_ganadas"] += 1
    elif resultado == -1:
        data[tipo_bot][color]["partidas_perdidas"] += 1
    else:
        data[tipo_bot][color]["partidas_empatadas"] += 1

    # Guardar los datos actualizados en el JSON
    with open(datos_qlearning, 'w') as file:
        json.dump(data, file, indent=2)



# Método para ver las estadísticas de los bots
def show_stadistics():
    print("ESTADÍSTICAS BOT RANDOM:")       
    read_stadistics_json(datos_random)
    print("\n---------------------------------------------------------------\n")       
    print("ESTADÍSTICAS BOT MONTE CARLO:")       
    read_stadistics_json(datos_montecarlo)
    print("\n---------------------------------------------------------------\n")       
    print("ESTADÍSTICAS BOT Q LEARNING:")       
    read_stadistics_json(datos_qlearning)


def read_stadistics_json(database):
    # Contadores
    total_games = 0
    total_wins = 0
    total_defeats = 0
    total_draws = 0
    
    # Se carga el json
    with open(database, 'r') as file:
        data = json.load(file)
    
    for bot, estadisticas in data.items():
        print(f"Estadísticas para partidas contra bot {bot}:")
        
        for color, datos_color in estadisticas.items():
            print(f"Color: {color}")
            print(f"Partidas jugadas: {datos_color['partidas_jugadas']}")
            print(f"Partidas ganadas: {datos_color['partidas_ganadas']}")
            print(f"Partidas perdidas: {datos_color['partidas_perdidas']}")
            print(f"Partidas empatadas: {datos_color['partidas_empatadas']}")
            print()

            # Actualizamos los contadores
            total_games += datos_color['partidas_jugadas']
            total_wins += datos_color['partidas_ganadas']
            total_defeats += datos_color['partidas_perdidas']
            total_draws += datos_color['partidas_empatadas']
    
    # Imprimir totales
    print("Totales:")
    print(f"Total de juegos: {total_games}")
    print(f"Total de victorias: {total_wins}")
    print(f"Total de derrotas: {total_defeats}")
    print(f"Total de empates: {total_draws}")


''' PRUEBAS
mod_stadistics_random("monte_carlo", "negras", 1)
mod_stadistics_random("random", "blancas", 0)
mod_stadistics_random("monte_carlo", "negras", -1)
mod_stadistics_montecarlo("qlearning", "negras", 1)
mod_stadistics_montecarlo("monte_carlo", "blancas", 0)
mod_stadistics_montecarlo("random", "negras", -1)
'''
#show_stadistics()
