from multiprocessing import freeze_support #Este import ayuda a trabajar con el multiproceso de firebase para mantener la db en tiempo real
from tkinter import ttk
from tkinter import *
from firebase import firebase


import sqlite3

class GeneradorContraseña:

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.resizable(0,0)
        self.wind.title('Generador de Contraseñas Ojai')
        self.wind.geometry("400x400")
        self.wind.iconbitmap(r'C:\\Users\\desarrollo.ti\\Desktop\\python_tkinter_app\\icon.ico')
        self.firebase = firebase.FirebaseApplication('https://pythondbgenerator.firebaseio.com/', None)
        ttk.Button(self.wind, text="Gestionar palabras", command=self.open_second_window).grid(row = 0, column = 1)
        Label(self.wind, text="Selecciona una palabra: ").grid(row=4, column=5)
        ttk.Combobox(self.wind)
        self.valor_combobox = StringVar() 
        self.select_word = ttk.Combobox(self.wind, width = 27, textvariable = self.valor_combobox, state='readonly') 
        self.obtener_palabras_combobox()
  
        self.select_word.grid(row = 5, column = 5 ) 
           

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Generar clave!')
        frame.grid(row = 6, column = 5, columnspan = 3, pady = 20)
        # Name Input
        Label(frame, text = 'Ingresa nombre y apellido: ').grid(row = 5, column = 1)
        self.full_name = Entry(frame)
        self.full_name.focus()
        self.full_name.grid(row = 7, column = 1)
    
        # Button Add Product 
        ttk.Button(frame, text = 'Generar', command = self.validar_palabra).grid(row = 8, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message_error = Label(text = '', fg = 'red', font="20")
        self.message_error.grid(row = 9, column = 5, columnspan = 2,  sticky = W + E)
        
        self.message_success = Label(text = '', fg = 'green', font="20")
        self.message_success.grid(row = 10, column = 5, columnspan = 2, sticky = W + E)

        
        self.click_open_second_wind = 0
        self.click_edit_key_word = 0
        
    
    def obtener_palabras_combobox(self):
        n = "cuidaremos"
        result =  self.firebase.get('/pythondbgenerator/Palabras', None)
        
        if result:
            palabras_clave = []
            lista_obj = list(result.values())
            for obj in lista_obj:
               palabras_clave.append(obj['Name'])
            
            self.select_word['values']  = tuple(palabras_clave)
            indice = 0
            if n in palabras_clave:
                indice = palabras_clave.index(n)
                self.select_word.current(indice)
            else:
                self.select_word.current(indice)

        else:
            print("No hay palabras clave")
            
    # Validar la palabra introducida por el usuario
    def validar_palabra(self):
        self.message_success["text"] = ""
        palabra_clave = self.valor_combobox.get()
        text_validate = ["1","2","3","4","5","6","7","8","9","0"]
        if self.full_name.get() == "":
            self.message_error['text'] = "arega un nombre y un apellido"
        elif len(self.full_name.get()) < 9:
            self.message_error['text'] = "agrega un nombre valido"
        elif len(self.full_name.get().split()) < 2:
            self.message_error['text'] = "agregar espacio entre cada palabra"
        elif len(self.full_name.get().split()) > 2:
            self.message_error['text'] = "No  agregar mas de un espacio"
        elif len(self.full_name.get().split()[0]) < 4:
            self.message_error['text'] = "El nombre debe tener mas de 3 letras"
        elif len(self.full_name.get().split()[1]) < 4:
            self.message_error['text'] = "El apellido debe tener mas de 3 letras"
        elif self.full_name.get().split()[0].isdigit():
            self.message_error['text'] = "El nombre no debe ser solo numeros"
        elif self.full_name.get().split()[1].isdigit():
            self.message_error['text'] = "El apellido no debe ser solo numeros"
        else:
            first_letter_name = self.full_name.get().split()[0][0].upper()
            name_split = self.full_name.get().split()[0][:4].lower()
            lastname_split = self.full_name.get().split()[1][:4].lower()
            
            is_number_in_string = False
            for i in text_validate:
                if i in self.full_name.get():
                    is_number_in_string = True
            if is_number_in_string:
                self.message_error['text'] = "No puedes mezclar numeros y letras"
            else:
                lista_name_letras = []
                lista_lastname_letras = []
                vueltas = 0
                for letra in name_split:
                        if letra in palabra_clave:
                            indice = palabra_clave.find(letra) + 1
                            
                            if indice == 10:
                                indice = 0
                            lista_name_letras.append(str(indice))
                            print(f"{indice} : {letra}")
                        else:
                            lista_name_letras.append(letra)
                for letra in lastname_split:
                    if letra in palabra_clave:
                        indice = palabra_clave.find(letra) + 1
                        if indice == 10:
                                indice = 0
                        lista_lastname_letras.append(str(indice))
                    else:
                        lista_lastname_letras.append(letra)
                
                lista_name_letras.append(".")
                lista_name_letras.pop(0)
                lista_name_letras.insert(0, first_letter_name)
                full_name_letras = lista_name_letras + lista_lastname_letras 
                
                convert_list_to_string = self.list_to_String(full_name_letras)
                self.message_error['text'] = ""  
                self.message_success['text'] = "Contraseña copiada \n \n {}".format(convert_list_to_string)
                self.wind.clipboard_clear()
                self.wind.clipboard_append(convert_list_to_string)
                self.wind.update()
                    
                
   
   
   #GESTION DE PALABRAS CLAVE
   #Lista a string
    def list_to_String(self,lista):
        str1 = ""
        
        return str1.join(lista)
    # Get Products from Database
    def obtenerDatos(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        result =  self.firebase.get('/pythondbgenerator/Palabras', None)
        if result:
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element) 
            #obtener datos
        
            # filling data
            palabras_dict = {}
            for key, value in result.items():
                self.tree.insert('', 0, text = key, values = value['Name'])
                palabras_dict[key] = value['Name']
            return palabras_dict
        else:
            print("Adios")

    def add_word(self):
        text_validate = ["1","2","3","4","5","6","7","8","9","0"]
        if self.name.get() == "":
            self.message_error2["text"] = "Agrega un valor"
        elif self.name.get().isdigit():
            self.message_error2["text"] = "No puedes agregar numeros"
        elif len(self.name.get()) < 8:
            self.message_error2["text"] = "La palabra debe tener mas de 8 letras"
        
        
        else:
            is_number_in_name = False
            for i in text_validate:
                if i in self.name.get():
                    is_number_in_name = True
            if is_number_in_name:
                self.message_error2["text"] = "No puedes mezclar numeros con letras"
            else:
                
                datos = {
                        'Name':self.name.get()
                        }
                lista_palabras = list(self.obtenerDatos().values())
                if lista_palabras:
                    print("lista_palabras",lista_palabras)
                    if self.name.get() in lista_palabras:
                            self.message_error2["text"] = "Ese nombre ya existe"
                            return False
                    else:
                            result =  self.firebase.post('/pythondbgenerator/Palabras', datos)
                            self.obtenerDatos()
                            self.obtener_palabras_combobox()
                            self.message_error2["text"] = ""
                            self.message_success2["text"] = "Palabra agregada"
                     
                else:
                    print("No hay palabras")
                   

    def delete_product(self):
        id_name = self.tree.item(self.tree.selection())['text']
        if id_name:
            print("id_name: ",id_name)
            print("id_name: ",id_name)
            self.firebase.delete('/pythondbgenerator/Palabras', id_name)
            print(id_name)
            self.obtenerDatos()
            print("Hola")
            self.obtener_palabras_combobox()
        else:
            self.message_success2["text"] = ""
            self.message_error2["text"] = "Selecciona una fila para borrar"
     

    def edit_product(self):
        self.click_edit_key_word = 1
        if self.click_edit_key_word > 1:
            pass
        else:
            try:
                self.id_name = self.tree.item(self.tree.selection())['text']
                self.name_row = self.tree.item(self.tree.selection())['values'][0]
            except IndexError:
                self.message_success2["text"] = ""
                self.message_error2["text"] = "Selecciona una fila para editar"
            else:
                self.edit_wind = Toplevel()
                self.edit_wind.title = 'Edit Product'
        
                # Old Name
                Label(self.edit_wind, text = 'Palabra clave: ').grid(row = 0, column = 1)
                Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = self.name_row), state = 'readonly').grid(row = 0, column = 2)
                # New Name
                Label(self.edit_wind, text = 'Nueva palabra: ').grid(row = 1, column = 1)
                new_name = Entry(self.edit_wind)
                new_name.grid(row = 1, column = 2)
                Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get())).grid(row = 4, column = 2, sticky = W)
                self.edit_wind.mainloop()
                self.click_edit_key_word = 0

    def edit_records(self, new_name):
        print("ID_NAME: {} NEW NAME: {}".format(self.id_name, new_name))
        result = self.firebase.put('/pythondbgenerator/Palabras/{}'.format(self.id_name), "Name",new_name)
        self.edit_wind.destroy()
        self.obtenerDatos()
        self.obtener_palabras_combobox()
        
    def open_second_window(self):
        self.click_open_second_wind += 1
        if self.click_open_second_wind > 1:
            pass
        else:
            self.second_window = Toplevel()
            self.second_window.title = 'Edit Product'
            self.second_window.resizable(0,0)
            

            frame = LabelFrame(self.second_window, text = 'Registrar una palabra clave')
            frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
            # Name Input
            Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
            self.name = Entry(frame)
            self.name.focus()
            self.name.grid(row = 1, column = 1)
            
            
            # Output Messages 
            self.message_error2 = Label(frame,text = '', fg = 'red', font="20")
            self.message_error2.grid(row = 2, column = 0, columnspan = 2,  sticky = W + E)
            
            self.message_success2 = Label(frame,text = '', fg = 'green', font="20")
            self.message_success2.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
            
            
            ttk.Button(frame, text = 'Agregar palabra clave', command = self.add_word).grid(row = 4, columnspan = 2, sticky = W + E)

            
            # Table
            self.tree = ttk.Treeview(frame, height = 10, columns = 2)
            self.tree.grid(row = 5, column = 0, columnspan = 2)
            self.tree.heading('#0', text = 'ID', anchor = CENTER)
            self.tree.heading('#1', text = 'PALABRA CLAVE', anchor = CENTER)
            
            ttk.Button(frame, text = 'DELETE', command = self.delete_product).grid(row = 6, column = 0, sticky = W + E)
            ttk.Button(frame, text = 'EDIT', command = self.edit_product).grid(row = 6, column = 1, sticky = W + E)

            self.obtenerDatos()
            self.second_window.protocol("WM_DELETE_WINDOW", self.cerrar_segunda_ventana)
    
            
    def cerrar_segunda_ventana(self):
        print("Se ha  cerrado la ventana")
        self.second_window.destroy()
        self.click_open_second_wind = 0

if __name__ == '__main__':
    
    freeze_support()
    
    window = Tk()
    application = GeneradorContraseña(window)
    window.mainloop()
