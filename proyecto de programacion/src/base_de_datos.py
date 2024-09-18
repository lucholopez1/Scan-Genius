import pandas as pd
import tkinter as tk
from tkinter import Menu, messagebox
import os
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#lista donde se guardaran todas las elecciones y modificaciones
datos = []

# Función para generar el ID concatenado y rellenarlo a 10 dígitos
def generar_id(marca, capacidad, fecha):
    # Diccionarios para los valores
    valores_marca = {"Apple": "100", "Samsung": "110", "Xiaomi": "111"}
    valores_capacidad = {"64GB": "100", "128GB": "110", "256GB": "111"}
    valores_fecha = {"2022/2024": "100", "2019/2021": "110", "2016/2018": "111"}

    # Obtener los valores correspondientes y concatenarlos
    id_marca = valores_marca[marca]
    id_capacidad = valores_capacidad[capacidad]
    id_fecha = valores_fecha[fecha]

    # Concatenar para formar el ID y rellenar con ceros a la izquierda para que tenga 10 dígitos
    id_concatenado = id_marca + id_capacidad + id_fecha  # Rellena con ceros si tiene menos de 10 dígitos

    return id_concatenado



#grupo de funciones que brinda la interfaz

#funcion que se encarga de verificar si un codigo ya se encuentra en la base de datos
def buscar_codigo():
    #codigo que se busca
    codigo_busqueda = generar_id(respuesta_opcion_marca.get().strip(), respuesta_opcion_almacenamiento.get().strip(), respuesta_opcion_modelo.get().strip())
    #se lee el archivo .csv que es la bse de datos y se busca que el codigo que se busca este en ella   
    archivo = pd.read_csv('base_de_datos.csv', delimiter=';')
    archivo['CODIGO'] = archivo['CODIGO'].astype(str).str.strip()  
     
    # en caso de estar o no en la base datos se sacan los siguientes datos: 
    if codigo_busqueda in archivo['CODIGO'].values:
        codigo_encontrado=True #un indicativo para saber si el codigo si fue encontrado
        resultado=archivo.isin([codigo_busqueda]) 
        posiciones = resultado[resultado].stack().index.tolist() #la posicion donde esta ubicado el codigo en la base de datos
        cantidad = archivo.loc[posiciones[0][0], 'CANTIDAD'] #la cantidad que corresponde de elementos para ese codigo
    # se sacan los mismo datos en este caso nulos porque no se encontro el codigo
    else:
        codigo_encontrado=False
        posiciones = 0
        cantidad= 0
    return codigo_encontrado, posiciones, cantidad, codigo_busqueda

#funcion para agregar datos a la base de datos
def agregar_seleccion():
    #se llama a la funcion de busqueda para saber si ese codigo ya esta en la base de datos
    codigo_encontrado, _, _, _=buscar_codigo() 
    
    #se crea la ventana para especificar el numero de unidades
    interfaz_numerica = tk.Tk()
    interfaz_numerica.title("Seleccionar valor")
    interfaz_numerica.geometry("200x100")
    
    #esta funcion retorna el valor numerico que el usuario escogio
    def numero():  
        valor = spinbox.get()
        return valor
    
    def agregar():
        #en caso de estar repetido se desplegara una ventana donde se podra especificar el numero de unidades que se desea agrega
        if codigo_encontrado==True:
            #todo esto modifica el valor de la columna de cantidad del codigo que se elijio deacuerdo al numero que elijio el usuario
            _, posiciones, cantidad, _=buscar_codigo() # se llaman los datos que se obtuvieron de la funcion de busqueda
            archivo = pd.read_csv('base_de_datos.csv', delimiter=';') #se lee la base datos
            nueva_cantidad=cantidad+int(numero()) #se crea el nuevo valor que tendra en la columna de cantidad
            codigo=generar_id(respuesta_opcion_marca.get().strip(), respuesta_opcion_almacenamiento.get().strip(), respuesta_opcion_modelo.get().strip())
            #se modifica la fila
            archivo.loc[posiciones[0][0]] ={
            "MARCA": respuesta_opcion_marca.get(),
            "ALMACENAMIENTO": respuesta_opcion_almacenamiento.get(),
            "MODELO": respuesta_opcion_modelo.get(),
            "CODIGO": codigo,
            "CANTIDAD": nueva_cantidad
            }
            archivo.to_csv('base_de_datos.csv', index=False, sep=';') # se guarda la modificacion
            interfaz_numerica.destroy() #se destruye la mini interfaz

        #en caso no estar en la base de datos se agregara un valor nueco a la base de datos    
        elif codigo_encontrado==False:
            #parametros del nuevo valor o fila
            cantidad= int(numero())
            codigo=generar_id(respuesta_opcion_marca.get().strip(), respuesta_opcion_almacenamiento.get().strip(), respuesta_opcion_modelo.get().strip())
            seleccion = {
            "MARCA": respuesta_opcion_marca.get(),
            "ALMACENAMIENTO": respuesta_opcion_almacenamiento.get(),
            "MODELO": respuesta_opcion_modelo.get(),
            "CODIGO": codigo,
            "CANTIDAD": cantidad
        }    
            #agrego el nuevo valor a la lista de datos para ser agregada a la base de datos
            datos.append(seleccion)
            interfaz_numerica.destroy()
    #parametros de la mini interfaz
    spinbox = tk.Spinbox(interfaz_numerica, from_=1, to=10)
    spinbox.pack(pady=10)
    boton = tk.Button(interfaz_numerica, text="Confirmar", command=agregar)
    boton.pack(pady=10)
    interfaz_numerica.mainloop()
    #parametros de la mini interfaz
    spinbox = tk.Spinbox(interfaz_numerica, from_=1, to=10)
    spinbox.pack(pady=10)
    boton = tk.Button(interfaz_numerica, text="Confirmar", command=agregar)
    boton.pack(pady=10)
    interfaz_numerica.mainloop()
    #mensaje de confirmacion
    messagebox.showinfo("Seleccionado", "Los datos han sido agregados correctamente")
#esta funcion se encarga de darle al usuario los datos acerca de la busqueda de un codgio en especifico    
def filtardo():
    codigo_encontrado, _, cantidad, codigo_buscado=buscar_codigo() #se llaman los datos de la funcion de busqeuda
    #en caso de ser encontrado se le mostrar en pantalla el codigo de su producto y el numero de unidades en stock
    if codigo_encontrado==True:
        messagebox.showinfo("busqueda en la base de datos", f"el producto se representa con el codigo {codigo_buscado} y se encuentran en stock {cantidad} unidades")
    #en caso de no ser encontrada en la base datos se le informara que no fue encontrada y su respectivo codigo
    else:
         messagebox.showinfo("error en busqueda", f"el producto de codigo {codigo_buscado} no se encuentra en la base de datos ")

#esta funcion sirve para guardar los datos recogidos en la funcion de gregar y adicionarlos o reemplazarlos en la base de datos
def guardar_selecciones():
    if datos: 
        df = pd.DataFrame(datos)
        
        archivo_existe = os.path.isfile('base_de_datos.csv')
        
        df.to_csv('base_de_datos.csv', mode='a', header=not archivo_existe, index=False, sep=';')
        print("Respuestas guardadas en 'base_de_datos.csv'.")
    else:
        print("No hay selecciones para guardar.")

#esta es la funcion para eliminar valores en la base de datos
def eliminar():
    codigo_encontrado, posiciones, _, _=buscar_codigo()# se llaman los datos de la funcion de busqueda
    #en caso de ser encontrado se le dara la opcion de borrar el producto por completo o solo modificar su cantidad en stock
    if codigo_encontrado==True: 
        #se crea una interfaz para dar la opcion
        mini_interfaz = tk.Tk()
        mini_interfaz.title("seleccione")
        #en caso de elegir el reseteo esta funcion con el dato de posicion eliminara esa fila
        def reseteo():
            archivo = pd.read_csv('base_de_datos.csv', delimiter=';')
            archivo=archivo.drop(posiciones[0][0])
            archivo.to_csv('base_de_datos.csv', index=False, sep=';')
            messagebox.showinfo("exito","se reseteo el producto con exito")
            mini_interfaz.destroy()
            
        #en caso de elegir eliminar por unidades se le preguntara por cuantas unidades desea restar y lo hara esta funcion
        def elemento():
            #se crea la pestaña para optener el numero de unidades
            unidades_restar = tk.Tk()
            unidades_restar.title("Seleccionar valor")
            unidades_restar.geometry("200x100")
                            #repite lo mismo que en la funcion agregar pero este restara las uniades a la columna cantidad
            def numero():  
                valor = spinbox.get()
                return valor            
            def eliminar_unidad():
                _, posiciones, cantidad, _=buscar_codigo()
                archivo = pd.read_csv('base_de_datos.csv', delimiter=';')
                nueva_cantidad = cantidad-int(numero())
                codigo=generar_id(respuesta_opcion_marca.get().strip(), respuesta_opcion_almacenamiento.get().strip(), respuesta_opcion_modelo.get().strip())
                archivo.loc[posiciones[0][0]] ={
                "MARCA": respuesta_opcion_marca.get(),
                "ALMACENAMIENTO": respuesta_opcion_almacenamiento.get(),
                "MODELO": respuesta_opcion_modelo.get(),
                "CODIGO": codigo,
                "CANTIDAD": nueva_cantidad
            }
                archivo.to_csv('base_de_datos.csv', index=False, sep=';')
                messagebox.showinfo("exito", "se elimino la unidad exitosamente")
                unidades_restar.destroy()
                mini_interfaz.destroy()
                                                  #parametros de las interfaz    
            spinbox = tk.Spinbox(unidades_restar, from_=1, to=10)
            spinbox.pack(pady=10)
            boton = tk.Button(unidades_restar, text="Confirmar", command=eliminar_unidad)
            boton.pack(pady=10)
            unidades_restar.mainloop()            
        boton1 = tk.Button(mini_interfaz, text="resetear", command=reseteo, bg="lightblue")
        boton2 = tk.Button(mini_interfaz, text="eliminar unidades", command=elemento, bg="lightgreen")
        boton1.grid(row=0, column=0, padx=10, pady=10)
        boton2.grid(row=0, column=1, padx=10, pady=10)
        mini_interfaz.mainloop()
    # en caso de encontrarse el codigo se le informara al usuario
    else:
        messagebox.showinfo("error", "el producto que desea eliminar nose encuentra en la base de datos")
    
# esta funcion le mostrar la tabla de datos al usuario
def abrir_archivo():
    root=tk.Tk()
    archivo = pd.read_csv('base_de_datos.csv', delimiter=';') 
    X= archivo.to_string(index=False, header=True, col_space=10)
    text_widget = ScrolledText(root, width=65, height=30)
    text_widget.pack(pady=10)
    text_widget.insert(tk.END, X)
    text_widget.config(state=tk.DISABLED)  
    
#funcion para cerrar la interfaz    
def cerrar():
    guardar_selecciones() #guarda todos los datos o acciones hechas con la funcion de guardar
    interfaz.destroy() #destruye la interfaz
# Crear la ventana principal
interfaz = tk.Tk()
interfaz.title("Interfaz de la Base de Datos")
interfaz.geometry("400x300")
interfaz.protocol("WM_DELETE_WINDOW", cerrar)

# -- Contenido principal de la ventana (Tres grupos de opción múltiple) --

# Grupo 1: Opción múltiple
respuesta_opcion_marca = tk.StringVar(value="none")  # Valor por defecto para el primer grupo
titulo_1 = tk.Label(interfaz, text="Seleccione la marca del dispositivo")
titulo_1.grid(row=0, column=0, columnspan=4, pady=10)

apple = tk.Radiobutton(interfaz, text="Apple", variable=respuesta_opcion_marca, value="Apple")
samsung = tk.Radiobutton(interfaz, text="Samsung", variable=respuesta_opcion_marca, value="Samsung")
xiaomi = tk.Radiobutton(interfaz, text="Xiaomi", variable=respuesta_opcion_marca, value="Xiaomi")

apple.grid(row=1, column=0, padx=10, pady=5)
samsung.grid(row=1, column=1, padx=10, pady=5)
xiaomi.grid(row=1, column=2, padx=10, pady=5)

# Grupo 2: Opción múltiple
respuesta_opcion_almacenamiento = tk.StringVar(value="none")  # Valor por defecto para el segundo grupo
titulo_2 = tk.Label(interfaz, text="Seleccione el almacenamiento del dispositivo")
titulo_2.grid(row=2, column=0, columnspan=4, pady=10)

gb64 = tk.Radiobutton(interfaz, text="64 GB", variable=respuesta_opcion_almacenamiento, value="64GB")
gb128 = tk.Radiobutton(interfaz, text="128 GB", variable=respuesta_opcion_almacenamiento, value="128GB")
gb256 = tk.Radiobutton(interfaz, text="256 GB", variable=respuesta_opcion_almacenamiento, value="256GB")

gb64.grid(row=3, column=0, padx=10, pady=5)
gb128.grid(row=3, column=1, padx=10, pady=5)
gb256.grid(row=3, column=2, padx=10, pady=5)

# Grupo 3: Opción múltiple
respuesta_opcion_modelo = tk.StringVar(value="none")  # Valor por defecto para el tercer grupo
titulo_3 = tk.Label(interfaz, text="Seleccione el rango de tiempo en que salió el dispositivo")
titulo_3.grid(row=4, column=0, columnspan=4, pady=10)

año_2022_2024 = tk.Radiobutton(interfaz, text="2022/2024", variable=respuesta_opcion_modelo, value="2022/2024")
año_2019_2021 = tk.Radiobutton(interfaz, text="2019/2021", variable=respuesta_opcion_modelo, value="2019/2021")
año_2016_2018 = tk.Radiobutton(interfaz, text="2016/2018", variable=respuesta_opcion_modelo, value="2016/2018")

año_2022_2024.grid(row=5, column=0, padx=10, pady=5)
año_2019_2021.grid(row=5, column=1, padx=10, pady=5)
año_2016_2018.grid(row=5, column=2, padx=10, pady=5)

# -- Botones organizados en una cuadrícula --
opcion_mostrar= tk.Button(interfaz, text="Base de datos", command=abrir_archivo, bg="red")
opcion_mostrar.grid(row=6, column=0, padx=10, pady=10)

opcion_buscar = tk.Button(interfaz, text="Buscar", command=filtardo, bg="lightgreen")
opcion_buscar.grid(row=6, column=1, padx=10, pady=10)

opcion_agregar = tk.Button(interfaz, text="Agregar", command=agregar_seleccion, bg="lightcoral")
opcion_agregar.grid(row=6, column=2, padx=10, pady=10)

opcion_eliminar = tk.Button(interfaz, text="Eliminar", command=eliminar, bg="lightyellow")
opcion_eliminar.grid(row=6, column=3, padx=10, pady=10)

menu1 = Menu(interfaz)
interfaz.config(menu=menu1)

def mostrar_grafico(tipo):
    try:
        # Leer los datos del archivo CSV
        archivo = pd.read_csv('base_de_datos.csv', delimiter=';')
        
        # Crear una nueva ventana para mostrar el gráfico
        ventana_grafico = tk.Toplevel(interfaz)
        ventana_grafico.title(f"Gráfico de {tipo.capitalize()}")
        
        # Crear la figura y el eje
        fig, ax = plt.subplots()

        # Generar el gráfico basado en el tipo seleccionado
        if tipo == 'barras':
            archivo.plot(kind='bar', x='CODIGO', y='CANTIDAD', ax=ax, legend=False)
            ax.set_ylabel('Cantidad')
        elif tipo == 'pastel':
            archivo.set_index('CODIGO')['CANTIDAD'].plot(kind='pie', ax=ax, autopct='%1.1f%%')

        ax.set_title(f"Gráfico de {tipo.capitalize()}")

        # Insertar el gráfico en la ventana de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'base_de_datos.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Agregar el menú a la interfaz principal
menu1 = Menu(interfaz)
interfaz.config(menu=menu1)

# Submenú para gráficos
grafico_menu = Menu(menu1, tearoff=0)
menu1.add_cascade(label="Gráficos", menu=grafico_menu)
grafico_menu.add_command(label="Gráfico de Barras", command=lambda: mostrar_grafico('barras'))
grafico_menu.add_command(label="Gráfico de Pastel", command=lambda: mostrar_grafico('pastel'))


# Iniciar el bucle principal de la ventana
interfaz.mainloop()

