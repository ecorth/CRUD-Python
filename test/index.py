from tkinter import ttk
from tkinter import * 

import sqlite3

class Producto:
    """
        Clase Producto encargada de todos los metodos de las ventanas
        contine una variable para llamar a la base de datos
    """
    db_nombre = 'almacen.db'
    """I-A
        Constructor de inicialización de ventana principal, 
        #1 Contenedor de elementos de la ventana
        #2 Etiqueta e input textbox de Producto
        #3 Etiqueta e input textbox de Precio
        #4 Menu de botones de operación a la base de datos
        #5 Mensaje mostrado para la operación a la base de datos
        #6 Tabla pqra visualizar los datos y llamada de función
    """
    def __init__(self,window):
        self.wind = window
        self.wind.title('Productos')
        #1
        frame = LabelFrame(self.wind, text = 'Nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #2
        Label(frame, text = 'Producto: ').grid(row = 1, column = 0)
        self.producto = Entry(frame)
        self.producto.focus()
        self.producto.grid(row = 1, column = 1)
        #3
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.precio = Entry(frame)
        self.precio.grid(row = 2, column = 1)
        #4
        ttk.Button(frame, text = 'Guardar', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = 'Eliminar', command = self.delete_product).grid(row = 4, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = 'Editar', command = self.edit_product).grid(row = 5, columnspan = 2, sticky = W + E)
        #5
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W+ E)
        #6
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Producto',anchor = CENTER)
        self.tree.heading('#1', text = 'Precio',anchor = CENTER)
        self.get_product()
    """I-B
        #1 Funcion de validacion de textbox completo
        #2 Funcion de consulta a la base de datos
        #3 Funcion de optanción de prodcutos 
        #4 Funcion para agregar registros de la base de datos
        #5 Funcion para borrar registros de la base de datos
    """ 
    #1   
    def validacion(self):
        return len(self.producto.get()) != 0 and len(self.precio.get()) != 0
    #2
    def query(self,query,parameters = ()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result
    #3
    def get_product(self):
        #limpieza de tabla
        registros = self.tree.get_children()
        for element in registros:
            self.tree.delete(element)
        query = 'SELECT * FROM producto ORDER BY producto DESC'
        db_rows =self.query(query)
        for row in db_rows:
            #print(row)
            self.tree.insert('',0, text = row[1], values = row[2])
    #4
    def add_product(self):
        if self.validacion():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
            parameters = (self.producto.get(), self.precio.get())
            self.query(query,parameters)
            self.mensaje['text'] = 'Producto {} agregado correctamente'.format(self.producto.get())
            self.producto.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje['text'] = 'Nombre y precio requerido'
        self.get_product()    
    #5
    def delete_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.mensaje['text'] = 'Selecciona un registro para borrar'
            return
        self.mensaje['text'] = ''
        producto = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM producto WHERE producto = ?'
        self.query(query, (producto, ))
        self.mensaje['text'] = 'Registro {} borrado correctamente'.format(producto)
        self.get_product()
    """I-C
        #1 Funcion para optener los productos a editar
        #2 Creacion de ventana emergente para la edicion de productos
        #3 Etiqueta e inputbox de Producto viejo y es solo lectura 
        #4 Etiqueta e inputbox de Producto nuevo
        #5 Etiquete e inputbox de Precio viejo y es solo lectura
        #6 Etiqueta e inputbox de Precio nuevo
        #7 Boton de oeparacion a la base de datos
        #8 Funcion para editar los registros en la base de datos
    """
    #1
    def edit_product(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except:
            self.mensaje['text'] = 'Selecciona un registro para editar'
            return
        producto = self.tree.item(self.tree.selection())['text']
        precio_viejo = self.tree.item(self.tree.selection())['values'][0]
        #2
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edición de Productos'
        #3
        Label(self.edit_wind, text = 'Producto:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = producto), state = 'readonly').grid(row = 0, column = 2)
        #4
        Label(self.edit_wind, text = 'Producto:').grid(row = 1, column = 1)
        nuevo_producto = Entry(self.edit_wind)
        nuevo_producto.grid(row = 1, column = 2)
        #5
        Label(self.edit_wind, text = 'Precio:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = precio_viejo), state = 'readonly').grid(row = 2, column = 2)
        #6
        Label(self.edit_wind, text = 'Precio:').grid(row = 3, column = 1)
        nuevo_precio= Entry(self.edit_wind)
        nuevo_precio.grid(row = 3, column = 2)
        #7
        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(nuevo_producto.get(), producto, nuevo_precio.get(), precio_viejo)).grid(row = 5 , column = 2, sticky = W)
        self.edit_wind.mainloop()
   #8 
    def edit_records(self, nuevo_producto, producto, nuevo_precio,precio_viejo):
        query = "UPDATE producto SET producto = ?, precio = ? WHERE producto = ? AND precio = ?"
        parameters = (nuevo_producto, nuevo_precio, producto, precio_viejo)
        self.query(query, parameters)
        self.edit_wind.destroy()
        self.mensaje['text'] = ' Registro {} actualizado correntamente'.format(producto)
        self.get_product()

if __name__ == '__main__':
    window = Tk()
    aplication = Producto(window)
    #window.geometry("500x400")
    window.mainloop()