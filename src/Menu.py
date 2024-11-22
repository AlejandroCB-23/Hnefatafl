# Librerías
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json
from Player import *
from Variable import *
import subprocess
import Board
from Game import *
from RandomBot import *	
from MonteCarloBot import *
from Q_Bot import *
import Board

'''
    Class Name: Menu
    Function: Gestionar la navegación por menús (comienzo de partidas, gestionar datos, resultados y salir).
'''


class Menu:
    # Constructor
    def __init__(self, user: Player):
        self.user = user # User identificado
        self.board_name = ""
        self.option_attacker : int
        self.option_defender : int
        self.n_iterations : int
        self.modo_juego = 0
        self.keep_running = True
        self.create_menu() # Crear el menú

    def create_menu(self):

        # Métodos

        # Hacer click en jugar, accede a la ventana para seleccionar modo de juego
        def click_play():
            select_gamemode_frame.place(x=455, y=45)  
            root_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            select_defender_frame.place_forget()
        
        # Usuario selecciona el modo de juego 1 vs 1 - se abre la pestaña para seleccionar rival
        def click_1_VS_1():
            select_gamemode_frame.place_forget() 
            root_frame.place_forget() 
            rival_selection_frame.place(x=455, y=45)
            frame_profile.place_forget()
            board_frame.place_forget()

        #Usuario selecciona el modo de juego 1 vs IA
        def click_1_VS_IA():
            select_gamemode_frame.place_forget() 
            root_frame.place_forget() 
            rival_and_Ia_selection_frame.place(x = 455, y = 45)
            frame_profile.place_forget()
            board_frame.place_forget()


        #Usuario selecciona el modo de juego IA vs IA

        # mostramos la pantalla para elegir el Bot atacante - Elegimos el modo de bot vs bot
        def click_bot_VS_bot_1() -> None:
            self.modo_juego = 4
            select_attacker_frame.place(x=455, y=45)  
            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_defender_frame.place_forget()

        
        # mostramos la pantalla para elegir el Bot defensor - Para el bot ataante hemos elegido la primera opcion
        def click_bot_VS_bot_at_op_0() -> None:
            self.option_attacker = 0
            select_defender_frame.place(x=455, y=45)  
            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            
            
        # mostramos la pantalla para elegir el Bot defensor - Para el bot ataante hemos elegido la segunda opcion
        def click_bot_VS_bot_at_op_1() -> None:
            self.option_attacker = 1
            select_defender_frame.place(x=455, y=45)  
            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
        
        # mostramos la pantalla para elegir el Bot defensor - Para el bot ataante hemos elegido la tercera opcion
        def click_bot_VS_bot_at_op_2() -> None:
            self.option_attacker = 2
            select_defender_frame.place(x=455, y=45)  
            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()


        # mostramos la pantalla para elegir el Bot defensor - Para el bot defensor hemos elegido la primera opcion
        def click_bot_VS_bot_def_op_0() -> None:
            self.option_defender = 0
            select_iterations_frame.place(x=455, y=45)

            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            

        # mostramos la pantalla para elegir el Bot defensor - Para el bot defensor hemos elegido la segunda opcion
        def click_bot_VS_bot_def_op_1() -> None:
            self.option_defender = 1
            select_iterations_frame.place(x=455, y=45)

            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            

        # mostramos la pantalla para elegir el Bot defensor - Para el bot defensor hemos elegido la tercera opcion
        def click_bot_VS_bot_def_op_2() -> None:
            self.option_defender = 2
            select_iterations_frame.place(x=455, y=45)

            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            

        # volvemos a la pantalla de seleccion del segundo bot, sin necesidad de volver a seleccionar el bot defensor
        def go_back_bot_2() -> None:
            select_defender_frame.place(x=455, y=45)

            root_frame.place_forget()
            select_gamemode_frame.place_forget() 
            board_frame.place_forget()
            frame_profile.place_forget()
            rival_selection_frame.place_forget()
            select_attacker_frame.place_forget()
            select_iterations_frame.place_forget()


        # Cuando el usuario selecciona el modo de juego 1
        def start_board_1():
            select_gamemode_frame.place_forget() 
            root_frame.place_forget() 
            board_frame.place_forget()
            self.board_name = "Brandubt"
            destroy_window()
            modo_selection()
            
        # Método para seleccionar el modo de juego
        def modo_selection ():
            if self.modo_juego == 0:
                Board.main(self.board_name, self.user.get_user()[0])
            if self.modo_juego == 1.1:
                Board.monte_carlo_bot(self.board_name, self.user.get_user()[0], 1)
            elif self.modo_juego == 1.2:
                Board.monte_carlo_bot(self.board_name, self.user.get_user()[0], 0)
            elif self.modo_juego == 2.1:
                Board.random_bot(self.board_name, self.user.get_user()[0], 1)
            elif self.modo_juego == 2.2:
                Board.random_bot(self.board_name, self.user.get_user()[0], 0)
            elif self.modo_juego == 3.1:
                Board.minmax_bot(self.board_name, self.user.get_user()[0], 1)
            elif self.modo_juego == 3.2:
                Board.minmax_bot(self.board_name, self.user.get_user()[0], 0)
            elif self.modo_juego == 4:
                start_board_bot_vs_bot_brandubt()

        def start_board_bot_vs_bot_brandubt() -> None:
            # Creacion del juego
            game = Game("Brandubt", str_json_game=TYPE_GAME)
            #Creacion de los bots
            if self.option_attacker == 0:
                bot_attack : RandomBot = RandomBot(game)
            elif self.option_attacker == 1:
                bot_attack : MonteCarloBot = MonteCarloBot(game)
            else:
                bot_attack : Q_Bot = Q_Bot(game,0)
                
        
            if self.option_defender == 0:
               bot_defense : RandomBot = RandomBot(game)
            elif self.option_defender == 1:
                bot_defense : MonteCarloBot = MonteCarloBot(game)
            else:
                bot_defense : Q_Bot = Q_Bot(game,1)
            
            Board.bot_vs_bot(game,bot_attack,bot_defense,self.n_iterations) # Iniciar el juego
        
        def verify_number():
            try:
                iterations = int(entry_iterations.get()) # lo parseamos a un numero entero
                if iterations > 0:
                    self.n_iterations = iterations
                    go_board_selection() # como el numero es valido, procedemos a elegir tablero
                else:
                    messagebox.showerror("Error", "El número de iteraciones debe ser mayor a 0.")
            except ValueError:
                messagebox.showerror("Error", "El número de iteraciones debe ser un número entero.")

        # Método para cerrar la ventana de Menu
        def destroy_window():
            root.destroy()
             
        # Método para cerrar la aplicación
        def on_closing():
            print("[EVENTO DETECTADO] CERRANDO APLICACION...........\n")
            self.keep_running = False
            root.destroy()
            root.quit() # Liberar recursos

        # Acceder a profile
        def click_profile():
            select_gamemode_frame.place_forget()  
            board_frame.place_forget()  
            frame_profile.place(x = 455, y = 45) 
            root_frame.place_forget()

        # Quitar y reiniciar
        def quit_and_restart():
            root.destroy()  # Cierra la ventana actual
            subprocess.run(["python", "src/main_2.py"])
            
        # Vuelta al menú principal
        def go_back_main_menu():
            select_gamemode_frame.place_forget() 
            rival_selection_frame.place_forget()
            rival_and_Ia_selection_frame.place_forget()
            frame_profile.place_forget()
            root_frame.place(x = 430, y = 45)

        # Ir a la selección de tablero
        def go_board_selection():
            select_gamemode_frame.place_forget() 
            rival_selection_frame.place_forget()
            frame_profile.place_forget()
            root_frame.place_forget()
            board_frame.place(x = 455, y = 45)


        
        # Cargar datos con los usuarios y las contraseñas
        def load_data():
            with open(os.path.dirname(os.path.abspath(__file__)) + "\\persistence\\users.json", 'r') as archivo:
                data = json.load(archivo)
            return data


        # Definir ventana
        root = Tk() 
        root.title("Hnefatafl") 
        root.geometry("925x500+300+200") 
        root.configure(bg = "#fff")
        root.resizable(False, False)    
        root.protocol("WM_DELETE_WINDOW", on_closing)  # Evento para cerrar la ventana

        # Cargar la imagen para icono go back
        back_icon = Image.open("src/assets/images/button_icons/button_regresar.png")
        back_icon = back_icon.resize((22, 22), Image.ADAPTIVE)
        image_back_profile = ImageTk.PhotoImage(back_icon)
       
        ###############################################################################################################################
        #   Frame root (menú con opciones principales)                                                                                #
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        root_frame = Frame(root, width=500, height=420, bg = "white")
        # Mostramos el frame root
        root_frame.place(x = 430, y = 45)

        # Título -> imagen
        img_root = PhotoImage(file = os.path.dirname(os.path.abspath(__file__)) + "/assets/images/icon_menu_root.png")
        img_root = img_root.subsample(2) # Redimension de imagen
        l_img_root = Label(root, image = img_root, bg = "white")
        l_img_root.place(x = 20, y = 30) # Mostramos la imagen

        # Subtítulo - ¿Qué desea hacer?
        subtitle_root = Label(root_frame, text="¿Qué desea hacer?", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        subtitle_root.place(x = 120, y = 0)


        #################################### Botón Jugar
        # Cargar la imagen
        play_icon = Image.open("src/assets/images/button_icons/button_jugar_icon.png")  # Icono para el botón
        play_icon = play_icon.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_play = ImageTk.PhotoImage(play_icon)

        # Crear el botón con la imagen
        play_button = Button(root_frame, image=imagen_play, compound="left", background= "#9E7488", command=click_play)
        play_button.pack(padx=10, pady=10)
        play_button.place(x = 90 , y = 50)


        #################################### Botón Historial
        # Cargar la imagen
        history_icon = Image.open("src/assets/images/button_icons/button_historial_icon.png")  # Icono para el botón
        history_icon = history_icon.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_history = ImageTk.PhotoImage(history_icon)

        # Crear el botón con la imagen
        history_button = Button(root_frame, image=imagen_history, compound="left", background= "#B0C8B1")
        history_button.pack(padx=10, pady=10)
        history_button.place(x = 250 , y = 50)

        #################################### Botón Perfil
        # Cargar la imagen
        perfil_icon = Image.open("src/assets/images/button_icons/button_perfil_icon.png")  # Icono para el botón
        perfil_icon = perfil_icon.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_perfil = ImageTk.PhotoImage(perfil_icon)

        # Crear el botón con la imagen
        perfil_button = Button(root_frame, image=imagen_perfil, compound="left", command=click_profile, background= "#9AB9DA")
        perfil_button.pack(padx=10, pady=10)
        perfil_button.place(x = 90 , y = 210)


        #################################### Botón Salir
        # Cargar la imagen
        salir_icon = Image.open("src/assets/images/button_icons/button_salir_icon.png")  # Icono para el botón
        salir_icon = salir_icon.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_salir = ImageTk.PhotoImage(salir_icon)

        # Crear el botón con la imagen
        salir_button = Button(root_frame, image=imagen_salir, compound="left", command=quit_and_restart, background= "#8978CE")
        salir_button.pack(padx=10, pady=10)
        salir_button.place(x = 250 , y = 210)



        ###############################################################################################################################
        #   Frame selección de modo de juego (1vs1, 1vsIA, IAvsIA)                                                                    #
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        select_gamemode_frame = Frame(root, width=500, height=800, bg = "white")
        
        # Subtítulo - Modo de juego
        subtitle_root = Label(select_gamemode_frame, text="Modo de Juego", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        subtitle_root.place(x = 120, y = 0)

        # Creación de botones (1vs1, 1vsIA, IAvsIA)
        #################################### Botón 1 VS 1
        # Cargar la imagen
        
        mode_1_icon = Image.open("src/assets/images/button_icons/button_1_VS_1_icon.png")  # Icono para el botón
        mode_1_icon = mode_1_icon.resize((222, 95), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        image_mode_1 = ImageTk.PhotoImage(mode_1_icon)

        # Crear el botón con la imagen
        mode_1_button = Button(select_gamemode_frame, image=image_mode_1, compound="left", command=click_1_VS_1, background= "#A6718D")
        mode_1_button.pack(padx=10, pady=10)
        mode_1_button.place(x = 108 , y = 50)
        

        #################################### Botón 1 VS IA
        # Cargar la imagen
        mode_2_icon = Image.open("src/assets/images/button_icons/button_1_VS_IA_icon.png")  # Icono para el botón
        mode_2_icon = mode_2_icon.resize((222, 95), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        image_mode_2 = ImageTk.PhotoImage(mode_2_icon)

        # Crear el botón con la imagen
        mode_2_button = Button(select_gamemode_frame, image=image_mode_2, compound="left",command=click_1_VS_IA, background= "#B0CEB9")
        mode_2_button.pack(padx=10, pady=10)
        mode_2_button.place(x = 108 , y = 155)
        

        #################################### Botón IA VS IA
        # Cargar la imagen
        mode_3_icon = Image.open("src/assets/images/button_icons/button_IA_VS_IA_icon.png")  # Icono para el botón
        mode_3_icon = mode_3_icon.resize((222, 95), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        image_mode_3 = ImageTk.PhotoImage(mode_3_icon)

        # Crear el botón con la imagen
        mode_3_button = Button(select_gamemode_frame, image=image_mode_3, compound="left",command=click_bot_VS_bot_1,background= "#89AEB5")
        mode_3_button.pack(padx=10, pady=10)
        mode_3_button.place(x = 108 , y = 260)

        ##############################  Boton regresar
        # Crear el botón con la imagen
        back_button = Button(select_gamemode_frame, image=image_back_profile, compound="left", command=go_back_main_menu, background="#fff")
        back_button.place(x=375, y=0)

        
        ###############################################################################################################################
        #   Frame selección de bot atacante (BOT VS BOT)                                                                    
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        select_attacker_frame = Frame(root, width=500, height=800, bg = "white")
        
        # Subtítulo - Modo de juego
        subtitle_root_attacker = Label(select_attacker_frame, text="Seleccione el BOT atacante", fg="black", bg="white", font=('Microsoft YaHei UI Light', 15, "bold"))
        subtitle_root_attacker.place(x = 80, y = 0)

        # Creación de botones (Random, MonteCarlo, Q-Learning)
        #################################### Botón Random

        # Crear el botón con la imagen
        button_random = Button(select_attacker_frame, text="RANDOM",compound="left",command=click_bot_VS_bot_at_op_0,background= "#A6718D",width=30,height=6)
        button_random.pack(padx=10, pady=10)
        button_random.place(x = 108 , y = 50)

        #################################### Botón MonteCarlo
        # Crear el botón con la imagen
        button_montecarlo = Button(select_attacker_frame, text="MONTECARLO", compound="left",command=click_bot_VS_bot_at_op_1,background= "#B0CEB9",width=30,height=6)
        button_montecarlo.pack(padx=10, pady=10)
        button_montecarlo.place(x = 108 , y = 155)        
        

        #################################### Botón Q-Learning
        # Crear el botón con la imagen
        button_select_ql = Button(select_attacker_frame, text="Q-LEARNING", compound="left",command=click_bot_VS_bot_at_op_2,background= "#89AEB5",width=30,height=6)
        button_select_ql.pack(padx=10, pady=10)
        button_select_ql.place(x = 108 , y = 260)

        ##############################  Boton regresar
        # Crear el botón con la imagen
        back_button_bot_att = Button(select_attacker_frame, image=image_back_profile, compound="left", command=click_play, background="#fff")
        back_button_bot_att.place(x=375, y=0)


        ###############################################################################################################################
        #   Frame selección de bot defensor (BOT VS BOT)                                                                    
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        select_defender_frame = Frame(root, width=500, height=800, bg = "white")
        
        # Subtítulo - Modo de juego
        subtitle_root_defender = Label(select_defender_frame, text="Seleccione el BOT defensor", fg="black", bg="white", font=('Microsoft YaHei UI Light', 15, "bold"))
        subtitle_root_defender.place(x = 80, y = 0)

        # Creación de botones (Random, MonteCarlo, Q-Learning)
        #################################### Botón Random
        # Crear el botón con la imagen
        button_random_2 = Button(select_defender_frame, text="RANDOM", compound="left",command=click_bot_VS_bot_def_op_0,background= "#A6718D",width=30,height=6)
        button_random_2.pack(padx=10, pady=10)
        button_random_2.place(x = 108 , y = 50)
        

        #################################### Botón MonteCarlo
        # Crear el botón con la imagen
        button_montecarlo_2 = Button(select_defender_frame, text="MONTECARLO", compound="left",command=click_bot_VS_bot_def_op_1,background= "#B0CEB9",width=30,height=6)
        button_montecarlo_2.pack(padx=10, pady=10)
        button_montecarlo_2.place(x = 108 , y = 155)
        

        #################################### Botón Q-Learning
        # Crear el botón con la imagen
        button_select_ql_2 = Button(select_defender_frame,text="Q-LEARNING", compound="left",command=click_bot_VS_bot_def_op_2,background= "#89AEB5",width=30,height=6)
        button_select_ql_2.pack(padx=10, pady=10)
        button_select_ql_2.place(x = 108 , y = 260)

        ##############################  Boton regresar
        # Crear el botón con la imagen
        back_button_bot_def = Button(select_defender_frame, image=image_back_profile, compound="left", command=click_bot_VS_bot_1, background="#fff")
        back_button_bot_def.place(x=375, y=0)

        ###############################################################################################################################
        #   Frame para seleccionar cuantos juegos se desean jugar                                                                    #                                                                    
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        select_iterations_frame = Frame(root, width=500, height=800, bg = "white")
        
        # Subtítulo - Modo de juego
        subtitle_root_iterations = Label(select_iterations_frame, text="Sesión de juego", fg="black", bg="white", font=('Microsoft YaHei UI Light', 15, "bold"))
        subtitle_root_iterations.place(x = 80, y = 0)

        txt_iterations = Label(select_iterations_frame, text="Seleccione el numero de iteraciones que quieres para la sesión", fg="black", bg="white", font=('Microsoft YaHei UI Light', 8, "bold"))
        txt_iterations.place(x = 80, y = 130)

        #################################### Botón Confirmación
        # Crear el botón con la imagen
        button_confirm = Button(select_iterations_frame, text="Confirmar", compound="left",command=verify_number,background= "#A6718D")
        button_confirm.pack(padx=10, pady=10)
        button_confirm.place(x = 308 , y = 180)

        # Crear cuadro de texto
        entry_iterations = Entry(select_iterations_frame, width=6,font=('Microsoft YaHei UI Light', 11) )
        entry_iterations.place(x = 180, y = 180)


        ##############################  Boton regresar
        # Crear el botón con la imagen
        back_button_iterations = Button(select_iterations_frame, image=image_back_profile, compound="left", command=go_back_bot_2, background="#fff")
        back_button_iterations.place(x=375, y=0)
        
        ###############################################################################################################################
        #   Ventana Rival Selection                                                                                                   #
        ###############################################################################################################################
        # Método que se inicia si el usuario hace click cuando ya ha seleccionado rival
        def rival_selected():
            if defender_list.size() == forward_list.size() == 1:
                go_board_selection()
            else:
                messagebox.showerror("Error", "Seleccione un rival.")


        # Se crea frame para elementos de la interfaz
        rival_selection_frame = Frame(root, width=500, height=800, bg = "white")
        self.modo_juego = 0

        # Subtítulo - Selección del rival
        subtitle_rival_selection = Label(rival_selection_frame, text="Selección de Rival", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        subtitle_rival_selection.place(x = 89, y = 0)
        
        # Botón para seleccionar rival
        Button(rival_selection_frame, width=32, pady=6, text="Seleccionar Rival", bg="black", fg="white", border=0, command=rival_selected).place(x=95, y=320)

        # Crear el botón para regresar
        rival_image_back = Button(rival_selection_frame, image=image_back_profile, compound="left", command=click_play, background="#fff")
        rival_image_back.place(x=375, y=0)

        # Data
        data = load_data()

        # Método para dar feedback cuando rival_list es seleccionado un elemento
        def rival_list_selected(event):
            # Obtener el índice del elemento seleccionado
            indice = rival_list.curselection()
            if indice:
                # Primero se borran las listas
                defender_list.delete(0, END)
                forward_list.delete(0, END)
                # Obtener el contenido del elemento seleccionado
                you = self.user.get_user()[0] + "   (Tú)"
                defender_list.insert(END, you)
                defender_list.insert(END, rival_list.get(indice[-1]))
                forward_list.insert(END, you)
                forward_list.insert(END, rival_list.get(indice[-1]))

        # Evento para manejar feedback con la lista de posibles defensores
        def defender_list_selected(event):
            if defender_list.size() == 2:
                # Obtener el índice del elemento seleccionado
                indice = defender_list.curselection()
                if indice:
                    if indice[-1] == 0:
                        defender_list.delete(1)
                        forward_list.delete(0)
                    else:
                        defender_list.delete(0)
                        forward_list.delete(1)
                        
        
        # Evento para manejar feedback con la lista de posibles atacantes
        def forward_list_selected(event):
                if forward_list.size() == 2:
                    # Obtener el índice del elemento seleccionado
                    indice= forward_list.curselection()
                    if indice:
                        if indice[-1] == 0:
                            forward_list.delete(1)
                            defender_list.delete(0)
                        else:
                            forward_list.delete(0)
                            defender_list.delete(1)


        # Crear el Listbox general
        rival_list = Listbox(rival_selection_frame, width=18, height=10, font=('Microsoft YaHei UI Light', 13))
        rival_list.place(x=30, y=50)
        # Vincular la función de controlador de evento al evento de selección
        rival_list.bind("<<ListboxSelect>>", rival_list_selected)

        # Subittle defenders
        subtitle_defender = Label(rival_selection_frame, text="Defensor 🛡️", fg="black", bg="white", font=('Microsoft YaHei UI Light', 14, "bold"))
        subtitle_defender.place(x = 220, y = 50)

        # Subittle atacante
        subtitle_forward = Label(rival_selection_frame, text="Atacante ⚔️", fg="black", bg="white", font=('Microsoft YaHei UI Light', 14, "bold"))
        subtitle_forward.place(x = 220, y = 200)

        # Crear el Listbox defensores
        defender_list = Listbox(rival_selection_frame, width=18, height=2, font=('Microsoft YaHei UI Light', 13))
        defender_list.place(x=220, y=90)
        defender_list.bind("<<ListboxSelect>>", defender_list_selected)

        # Crear el Listbox atacante
        forward_list = Listbox(rival_selection_frame, width=18, height=2, font=('Microsoft YaHei UI Light', 13))
        forward_list.place(x=220, y=240)
        forward_list.bind("<<ListboxSelect>>", forward_list_selected)


        # Extraer los nombres de usuario
        rivals = [usuario["name"] for usuario in data["users"]]
        
        # Agregar los nombres de los posibles rivales al Listbox
        for r in rivals:
            if r != self.user.get_user()[0]:
                rival_list.insert(END, r)




        ###############################################################################################################################
        #   Ventana Rival_and_Ia Selection                                                                                                   #
        ###############################################################################################################################

        # Método para manejar la selección del rol (atacante o defensor)
        def select_role(role):
            global selected_role
            selected_role = role

        # Método para manejar la selección del bot y confirmar la selección
        def confirm_selection():
            global selected_bot, selected_role
            selected_bot = bot_list.get(bot_list.curselection()[0]) if bot_list.curselection() else None
            if selected_bot and selected_role:
                messagebox.showinfo("Confirmación", f"Bot seleccionado: {selected_bot}\nBot Rol seleccionado: {selected_role}\n{self.user.get_user()[0]}: {('Defensor' if selected_role == 'Atacante' else 'Atacante')}")
                # Aquí podrías hacer lo que necesites con la selección, como pasarla a la siguiente ventana o realizar alguna otra acción

                if selected_bot == "Montecarlo":
                    if selected_role == "Atacante":
                        self.modo_juego = 1.2
                    else:
                        self.modo_juego = 1.1

                elif selected_bot == "Random":
                    if selected_role == "Atacante":
                        self.modo_juego = 2.2
                    else:
                        self.modo_juego = 2.1

                elif selected_bot == "Minimax":
                    if selected_role == "Atacante":
                        self.modo_juego = 3.2
                    else:
                        self.modo_juego = 3.1

                go_board_selection()

            else:
                messagebox.showerror("Error", "Seleccione un bot y un rol.")


        # Crear una nueva ventana similar a rival_selection_frame para seleccionar bots y roles
        rival_and_Ia_selection_frame = Frame(root, width=500, height=800, bg="white")

        # Subtítulo - Selección de Bot y Rol
        subtitle_rival_selection = Label(rival_and_Ia_selection_frame, text="Selección de Bot y Rol", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        subtitle_rival_selection.place(x=45, y=0)

        # Listbox para mostrar los bots disponibles
        bot_list = Listbox(rival_and_Ia_selection_frame, width=18, height=10, font=('Microsoft YaHei UI Light', 13))
        bot_list.place(x=80, y=50)

        # Botones de selección de rol (atacante o defensor)
        attacker_button = Button(rival_and_Ia_selection_frame, text="Atacante", bg="#7FFF00", fg="black", command=lambda: select_role("Atacante"))
        attacker_button.place(x=80, y=300)

        defender_button = Button(rival_and_Ia_selection_frame, text="Defensor", bg="#FF6347", fg="black", command=lambda: select_role("Defensor"))
        defender_button.place(x=180, y=300)

        # Botón de confirmar selección
        confirm_button = Button(rival_and_Ia_selection_frame, text="Confirmar", bg="black", fg="white", command=confirm_selection)
        confirm_button.place(x=80, y=350)

        # Botón de regresar
        rival_and_Ia_back_button = Button(rival_and_Ia_selection_frame, image=image_back_profile, compound="left", command=go_back_main_menu, background="#fff")
        rival_and_Ia_back_button.place(x=375, y=0)

        # Método para cargar la lista de bots disponibles
        def load_bots():
            # Aquí cargarías la lista de bots desde donde sea que los estés almacenando
            bots = ["Random", "Montecarlo", "Minimax", "Q-learning"]  # Por ejemplo, una lista de nombres de bots
            for bot in bots:
                bot_list.insert(END, bot)

        # Llamar al método para cargar los bots disponibles
        load_bots()





        ###############################################################################################################################
        #   Frame board (menú para seleccionar el tipo de tablero)                                                                    #
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        board_frame = Frame(root, width=500, height=800, bg = "white")

        # Subtítulo - Tablero
        subtitle_board = Label(board_frame, text="Selección de Tablero", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        subtitle_board.place(x = 55, y = 0)


        #################################### Tablero 1
        # Cargar la imagen
        board_1 = Image.open("src/assets/images/button_icons/game_mode_1_board.png")  # Icono para el botón
        board_1 = board_1.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_board_1 = ImageTk.PhotoImage(board_1)

        # Crear el botón con la imagen
        board_1_button = Button(board_frame, image=imagen_board_1, compound="left", background= "White" , command=start_board_1)
        board_1_button.pack(padx=10, pady=10)
        board_1_button.place(x = 20, y = 50)

        #################################### Tablero 2
        # Cargar la imagen
        board_2 = Image.open("src/assets/images/button_icons/game_mode_2_board.png")  # Icono para el botón
        board_2 = board_2.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_board_2 = ImageTk.PhotoImage(board_2)

        # Crear el botón con la imagen
        board_2_button = Button(board_frame, image=imagen_board_2, compound="left", background= "White")
        board_2_button.pack(padx=10, pady=10)
        board_2_button.place(x = 200 , y = 50)

        #################################### Tablero 3
        # Cargar la imagen
        board_3 = Image.open("src/assets/images/button_icons/game_mode_3_board.png")  # Icono para el botón
        board_3 = board_3.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_board_3 = ImageTk.PhotoImage(board_3)

        # Crear el botón con la imagen
        board_3_button = Button(board_frame, image=imagen_board_3, compound="left", background= "White")
        board_3_button.pack(padx=10, pady=10)
        board_3_button.place(x = 20 , y = 230)


        #################################### Tablero 4
        # Cargar la imagen
        board_4 = Image.open("src/assets/images/button_icons/game_mode_4_board.png")  # Icono para el botón
        board_4 = board_4.resize((150, 150), Image.ADAPTIVE)  # Redimensionar la imagen según sea necesario
        imagen_board_4 = ImageTk.PhotoImage(board_4)

        # Crear el botón con la imagen
        board_4_button = Button(board_frame, image=imagen_board_4, compound="left", background= "White")
        board_4_button.pack(padx=10, pady=10)
        board_4_button.place(x = 200 , y = 230)


        ##############################  Boton regresar
        # Crear el botón con la imagen
        board_back_button = Button(board_frame, image=image_back_profile, compound="left", command=click_play, background="#fff")
        board_back_button.place(x=375, y=0)

        

        ###############################################################################################################################
        #   Ventana Profile                                                                                                           #
        ###############################################################################################################################
        # Método para modificar las credenciales del usuario conectado
        def mod_profile():
            if mod_passw.get() == "" or repeat_mod_passw.get() == "":
                messagebox.showerror("Error", "Complete todos los campos")
            else:   
                if mod_passw.get() != repeat_mod_passw.get():
                    messagebox.showerror("Error", "Las contraseñas no coinciden.")
                else:
                    data = load_data()
                    for user in data['users']:
                        if user['name'] == self.user.get_user()[0]:
                            user['password'] = mod_passw.get()

                    # Guardar el JSON actualizado
                    with open(os.path.dirname(os.path.abspath(__file__)) + "\\persistence\\users.json", 'w') as file:
                        json.dump(data, file, indent=4)
                    
                    messagebox.showinfo("Notificación", "Cambios aplicados.") # Notificación al usuario


        
        # Método para borrar el perfil del usuario conectado
        def delete_profile():
            result = messagebox.askokcancel("Mensaje de Confirmación", "¿Estás seguro que deseas borrar la cuenta?")
            if result:
                messagebox.showinfo("Notificación", "Cuenta borrada.") # Notificación al usuario
                data = load_data()
                for user in data['users']:
                    if user['name'] == self.user.get_user()[0]:
                        data['users'].remove(user) # Se borra el usuario

                # Guardar el JSON actualizado
                with open(os.path.dirname(os.path.abspath(__file__)) + "\\persistence\\users.json", 'w') as file:
                    json.dump(data, file, indent=4)
                
                # Se vuelve al inicio de la aplicación
                destroy_window()

            else:
                messagebox.showinfo("Notificación", "Operación cancelada.") # Notificación al usuario



        # Se crea frame para elementos de la interfaz para modificar los valores del perfil del usuario registrado
        frame_profile = Frame(root, width=500, height=600, bg = "white")

        # Cabecera
        heading_mod_p = Label(frame_profile, text="Mi Perfil", fg="black", bg="white", font=('Microsoft YaHei UI Light', 20, "bold"))
        heading_mod_p.place(x = 176, y = 0)

        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Nombre de usuario (disabled)
        id_user = Entry(frame_profile, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        id_user.place(x = 90, y = 80)
        id_user.insert(0, self.user.get_user()[0])
        id_user.config(state='disabled')
        Frame(frame_profile, width=295, height=2, bg = "black").place(x=85, y = 107)


        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Contraseña a modificar
        mod_passw = Entry(frame_profile, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        mod_passw.place(x=90, y=150)
        mod_passw.insert(0, self.user.get_user()[1])

        Frame(frame_profile, width=295, height=2, bg = "black").place(x=85, y=177)

        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Entrada para repetir contraseña modificada
        repeat_mod_passw = Entry(frame_profile, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        repeat_mod_passw.place(x=90, y=220)
        repeat_mod_passw.insert(0, self.user.get_user()[1])

        Frame(frame_profile, width=295, height=2, bg = "black").place(x=85, y=247)

        ###################----------------------------------------------------------------------------------------------------------------------###################

        # Botón para modificar credenciales
        Button(frame_profile, width=39, pady=7, text="Modificar Credenciales", bg="black", fg="white", border=0, command=mod_profile).place(x=95, y=274)

        # Botón para borrar usuario
        Button(frame_profile, width=15, text="Borrar Cuenta", bg="#8B0000", fg="white", border=0, command=delete_profile).place(x=340, y=400)
        
        ##############################  Boton regresar
        # Crear el botón con la imagen
        profile_image_back = Button(frame_profile, image=image_back_profile, compound="left", command=go_back_main_menu, background="#fff")
        profile_image_back.place(x=375, y=0)

        
        root.mainloop() # Loop de la ventana
        
        
        
