# Scan-Genius
Proyecto final de programación desarrollado por Rafael Gallardo, Juan López y Luis López.
Este proyecto implementa una interfaz gráfica en Python usando tkinter para gestionar una base de datos de productos,
permitiendo realizar operaciones como agregar, buscar, eliminar y mostrar productos. Los datos se almacenan en un
archivo CSV (base_de_datos.csv) y el proyecto incluye la generación de gráficos con matplotlib para visualizar el
inventario.

# Características
Buscar productos: Permite buscar un producto por su ID único generado.

Agregar productos: Se puede agregar un nuevo producto o actualizar la cantidad de uno existente.

Eliminar productos: Elimina un producto completamente o reduce la cantidad en stock.

Visualizar base de datos: Muestra todo el contenido de la base de datos en una ventana de desplazamiento.

Generación de gráficos: Permite visualizar los productos en gráficos de barras o de pastel.

# Requisitos
Python 3.x
Librerías necesarias:
pandas
tkinter
matplotlib

# Interfaz:

Agregar producto: Selecciona la marca, almacenamiento y modelo, y elige la cantidad para agregar.

Buscar producto: Busca un producto en la base de datos usando la combinación de sus características.

Eliminar producto: Puedes eliminar el producto completamente o restar una cantidad.

Visualizar base de datos: Muestra todos los productos y sus cantidades.

Generar gráficos: Puedes generar gráficos de barras o pastel que muestran la distribución de los productos.

# Archivos
base_de_datos.py: Archivo principal del proyecto con toda la lógica de la aplicación.

base_de_datos.csv: Archivo CSV que contiene la base de datos de productos.
