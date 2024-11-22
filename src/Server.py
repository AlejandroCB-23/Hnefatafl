# Librerías
from tkinter import *
from tkinter import messagebox
import os
import json
from Variable import *
from Player import *

'''
    Class Name: Server
    Function: Clase para gestionar el acceso de los usuarios (dar de alta y acceder al juego)
'''
class Server:
    # Constructor
    def __init__(self):
        self.valid = False # ¿Usuario válido?
        self.player = Player() # User
        self.create_server() # Generamos el servidor

    def create_server(self):

        # Método para cerrar la ventana de Server
        def destroy_window():
            root.destroy() 
            


        # Cargar datos con los usuarios y las contraseñas
        def load_data():
            with open(os.path.dirname(os.path.abspath(__file__)) + "\\persistence\\users.json", 'r') as archivo:
                data = json.load(archivo)
            return data



        # Cambiar de ventana al frame de crear cuenta
        def switch_to_create_account():
            frame.place_forget() # Ocultamos el frame de login
            frame_create_account.place(x = 480, y = 70) # Mostramos el frame para crear cuenta 

            # Se muesta la imagen de la ventana de crear cuenta (se oculta la de login)
            l_img_2.place(x = 20, y = 30)
            l_img_1.place_forget()

            # Se actualizan los campos de texto
            update_text_fiels()




        # Cambiar de ventana al frame de login
        def switch_to_login():
            frame.place(x = 480, y = 70) # Mostramos el frame de login
            frame_create_account.place_forget() # Ocultamos el frame para crear cuenta 
            
            # Se muesta la imagen de la ventana de login (se oculta la de crear cuenta)
            l_img_1.place(x = 20, y = 30)
            l_img_2.place_forget()
            
            # Se actualizan los campos de texto
            update_text_fiels()




        # Actualizar las cajas de texto
        def update_text_fiels():
            # Ventana login
            user.delete(0, "end")
            user.insert(0, "Usuario")
            passw.delete(0, "end")
            passw.insert(0, "Contraseña")
            # Ventana crear cuenta
            create_user.delete(0,"end")
            create_user.insert(0, "Nuevo Usuario")
            create_passw.delete(0, "end")
            create_passw.insert(0, "Contraseña")
            repeat_passw.delete(0, "end")
            repeat_passw.insert(0, "Repetir Contraseña")



        # Comprobar credenciales
        def signin():
            data = load_data()
            u = user.get()
            p = passw.get()
            cont = False
            for user_data in data['users']:
                # Comprobar si el nombre de usuario y la contraseña coinciden
                if user_data['name'] == u and user_data['password'] == p:
                    messagebox.showinfo("Notificación", "Acceso validado.") # Notificación al usuario
                    cont = True
                    self.valid = True # Usuario válido
                    self.player.mod_user(u,p)
                    
                    destroy_window()   
            if not cont:
                messagebox.showerror("Error", "Credenciales incorrectas.")


        # Crear nueva cuenta
        def create_account():
            # Se carga la información de las cajas de texto
            new_user = create_user.get()
            new_pass = create_passw.get()
            repeat_new_pass = repeat_passw.get()

            # Primero se comprueba que las contraseñas coincidan
            if new_pass == repeat_new_pass:
                # Los campos deben estar rellenados correctamente
                if not (new_user == "" or new_pass == ""):
                    # Si se da este caso, se debe comprobar que no exista un usuario con ese user (user es el identificador de cada usuario)
                    data = load_data()
                    exist = False
                    for user_data in data['users']:
                        if user_data['name'] == new_user:
                            exist = True
                            print("Existe")
                    if not exist: # Si no existe se crea la cuenta
                        # Se crea el nuevo usuario
                        new_user = {"name": new_user, "password": new_pass}
                        data["users"].append(new_user)

                        # Guardar el archivo actualizado
                        with open(os.path.dirname(os.path.abspath(__file__)) + "\\persistence\\users.json", 'w') as file:
                            json.dump(data, file, indent=4)

                        # Se vuelve a la pestaña de login
                        messagebox.showinfo("Notificación", "¡Cuenta creada correctamente!") # Notificación al usuario
                        switch_to_login()
                    else:
                        messagebox.showerror("Error", "El usuario ya existe.")
                else:
                    messagebox.showerror("Error", "Rellene correctamente todos los campos.")
            else:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")

        # Definir ventana
        root = Tk() 
        root.title("Hnefatafl") 
        root.geometry("925x500+300+200") 
        root.configure(bg = "#fff")
        root.resizable(False, False)    

        # Imagen de fondo (1-login)
        img_1 = PhotoImage(file = os.path.dirname(os.path.abspath(__file__)) + "/assets/images/icon_login_window.png")
        img_1 = img_1.subsample(2) # Redimension de imagen
        l_img_1 = Label(root, image = img_1, bg = "white")
        l_img_1.place(x = 20, y = 30) # Mostramos la imagen

        # Imagen de fondo (2-create_account)
        img_2 = PhotoImage(file = os.path.dirname(os.path.abspath(__file__)) + "/assets/images/icon_create_account_window.png")
        img_2 = img_2.subsample(2) # Redimension de imagen
        l_img_2 = Label(root, image = img_2, bg = "white") # No se muestra de momento



        ###############################################################################################################################
        #   Ventana Login                                                                                                             #
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz
        frame = Frame(root, width=350, height=350, bg = "white")
        frame.place(x = 480, y = 70)

        # Cabecera
        heading = Label(frame, text="Inicio Sesión", fg="black", bg="white", font=('Microsoft YaHei UI Light', 26, "bold"))
        heading.place(x = 110, y = 4)

        ###################----------------------------------------------------------------------------------------------------------------------###################

        # Entrada de usuario
        def on_enter(e): # Si haces click en la caja de texto user
            user.delete(0, "end")
        def on_leave(e):
            if user.get() == "":
                user.insert(0, "Usuario") # Si dejas de hacer "focus" en la caja de texto user

        user = Entry(frame, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        user.place(x = 90, y = 80)
        user.insert(0, "Usuario")
        user.bind('<FocusIn>', on_enter) # Focus 
        user.bind('<FocusOut>', on_leave) # Not focus

        Frame(frame, width=295, height=2, bg = "black").place(x=85, y = 107)

        ###################----------------------------------------------------------------------------------------------------------------------###################

        # Entrada de contraseña
        def on_enter(e): # Si haces click en la caja de texto passw
            passw.delete(0, "end")
        def on_leave(e):
            if passw.get() == "":
                passw.insert(0, "Contraseña") # Si dejas de hacer "focus" en la caja de texto passw

        passw = Entry(frame, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        passw.place(x=90, y=150)
        passw.insert(0, "Contraseña")
        passw.bind("<FocusIn>", on_enter) # Focus
        passw.bind("<FocusOut>", on_leave) # Not Focus

        Frame(frame, width=295, height=2, bg = "black").place(x=85, y=177)

        ###################----------------------------------------------------------------------------------------------------------------------###################

        # Botón para acceder con las credenciales
        Button(frame, width=39, pady=7, text="Acceder", bg="black", fg="white", border=0, command=signin).place(x=85, y=204)

        # Label para poder crear cuenta
        label_create_account = Label(frame, text = "¿No tienes una cuenta?" , fg="black", bg="white", font=('Microsoft YaHei UI Light', 9))
        label_create_account.place(x=85, y=270)

        # Botón para acceder al formulario de crear una cuenta nueva
        button_create_account = Button(frame, width=9, text= "Crear cuenta", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=switch_to_create_account)
        button_create_account.place(x=230, y=271.2)



        ###############################################################################################################################
        #   Ventana Create Account                                                                                                    #
        ###############################################################################################################################
        # Se crea frame para elementos de la interfaz de crear cuenta
        frame_create_account = Frame(root, width=350, height=400, bg = "white")

        # Cabecera
        heading_c = Label(frame_create_account, text="Crear Cuenta", fg="black", bg="white", font=('Microsoft YaHei UI Light', 26, "bold"))
        heading_c.place(x = 100, y = 4)

        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Entrada de nuevo nombre de usuario
        def on_enter(e): # Si haces click en la caja de texto 
            create_user.delete(0, "end")
        def on_leave(e):
            if create_user.get() == "":
                create_user.insert(0, "Nuevo Usuario") # Si dejas de hacer "focus" en la caja de texto 

        create_user = Entry(frame_create_account, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        create_user.place(x = 90, y = 80)
        create_user.insert(0, "Nuevo Usuario")
        create_user.bind('<FocusIn>', on_enter) # Focus 
        create_user.bind('<FocusOut>', on_leave) # Not focus

        Frame(frame_create_account, width=295, height=2, bg = "black").place(x=85, y = 107)


        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Entrada de contraseña nueva
        def on_enter(e): # Si haces click en la caja de texto passw
            create_passw.delete(0, "end")
        def on_leave(e):
            if create_passw.get() == "":
                create_passw.insert(0, "Contraseña") # Si dejas de hacer "focus" en la caja de texto passw

        create_passw = Entry(frame_create_account, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        create_passw.place(x=90, y=150)
        create_passw.insert(0, "Contraseña")
        create_passw.bind("<FocusIn>", on_enter) # Focus
        create_passw.bind("<FocusOut>", on_leave) # Not Focus

        Frame(frame_create_account, width=295, height=2, bg = "black").place(x=85, y=177)

        ###################----------------------------------------------------------------------------------------------------------------------###################
        # Entrada para repetir contraseña nueva
        def on_enter(e): # Si haces click en la caja de texto passw
            repeat_passw.delete(0, "end")
        def on_leave(e):
            if repeat_passw.get() == "":
                repeat_passw.insert(0, "Repetir Contraseña") # Si dejas de hacer "focus" en la caja de texto passw

        repeat_passw = Entry(frame_create_account, width=25, fg="black", border="0", bg="white", font=('Microsoft YaHei UI Light', 11) )
        repeat_passw.place(x=90, y=220)
        repeat_passw.insert(0, "Repetir Contraseña")
        repeat_passw.bind("<FocusIn>", on_enter) # Focus
        repeat_passw.bind("<FocusOut>", on_leave) # Not Focus

        Frame(frame_create_account, width=295, height=2, bg = "black").place(x=85, y=247)

        ###################----------------------------------------------------------------------------------------------------------------------###################

        # Botón para crear cuenta
        Button(frame_create_account, width=39, pady=7, text="Crear Cuenta", bg="black", fg="white", border=0, command=create_account).place(x=85, y=274)

        # Label para poder acceder a la ventana login
        label_access = Label(frame_create_account, text = "¿Ya tienes una cuenta?" , fg="black", bg="white", font=('Microsoft YaHei UI Light', 9))
        label_access.place(x=85, y=340)

        # Botón para acceder al formulario de crear una cuenta nueva
        button_access_login = Button(frame_create_account, width=9, text= "Acceder", border=0, bg="white", cursor="hand2", fg="#57a1f8", command=switch_to_login)
        button_access_login.place(x=230, y=341.5)

        root.mainloop() # Loop de la ventana
        root.quit() # Liberar recursos
        
        

