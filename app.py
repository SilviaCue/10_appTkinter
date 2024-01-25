from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        # Habilita la redimensión y (0,0) la deshabilita
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre")
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # label Precio
        self.etiqueta_precio = Label(frame, text="Precio")
        self.etiqueta_precio.grid(row=2, column=0)

        # Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoría")
        self.etiqueta_categoria.grid(row=3, column=0)

        # Entry categoría
        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1)

        # Botón añadir Producto
        self.boton_aniadir = ttk.Button(
            frame, text="Guardar Producto", command=self.add_producto)
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Mensaje informativo usuario
        self.mensaje = Label(text="", fg="CadetBlue", font=("bold",))
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Tabla de productos

        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla

        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))

        # Se  modifica la  fuente de las  cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {
                     'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(
            height=20, columns=3, style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=3)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1
        try:
            self.tabla.heading('#2', text="Categoría",
                               anchor=CENTER)  # Encabezado 2
        except Exception as e:
            print("Error en encabezado: {}".format(e))

        # botones de editar y eliminar
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto)
        boton_eliminar.grid(row=6, column=0, sticky=W + E)
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto)
        boton_editar.grid(row=6, column=2, sticky=W + E)

        # invocar get_productos
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
            return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            print(fila)

            self.tabla.insert("", 0, text=fila[1], values=fila[2:4])

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def validacion_categoria(self):
        return len(self.categoria.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?,?,?)"
            parametros = (self.nombre.get(), self.precio.get(),
                          self.categoria.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "Producto {} añadido con éxito ".format(
                self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False:
            print("La categoría es obligatoria")
            self.mensaje["text"] = "La categoría es obligatoria"

        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El  nombre es obligatorio"

        elif self.validacion_categoria() == False and self.validacion_categoria():
            print("La categoría es obligatoria")
            self.mensaje["text"] = "La categoría es obligatoria"

        else:
            print("El nombre, el precio y la categoría son obligatorios")
            self.mensaje["text"] = "El nombre, el precio y la categoría son obligatorios"
        self.get_productos()

    def del_producto(self):
        print("Eliminar producto")
        self.mensaje["text"] = ("")
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre =?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "Producto {} eliminado con éxito".format(nombre)
        self.get_productos()

    def edit_producto(self):
        print("Editar producto")
        self.mensaje["text"] = ("")
        old_nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]
        old_categoria = self.tabla.item(self.tabla.selection())["values"][1]

        self.ventana_editar = Toplevel()  # Crear una ventana nueva
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=(
            "Calibri", 30, "bold"))
        titulo.grid(row=1, column=0, columnspan=20, pady=20)

        frame_ep = LabelFrame(self.ventana_editar,
                              text="Editar el siguiente Producto")
        frame_ep.grid(row=2, column=0, columnspan=20, pady=20)

        # Label del nombre antiguo
        self.antiguo_nombre = Label(
            frame_ep, text="Nombre antiguo", font=("Calibri", 13))
        self.antiguo_nombre.grid(row=2, column=0)

        # Entry o input del nombre antiguo
        self.input_antiguo_nombre = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre),
                                          state="readonly", font=("Calibri", 13))
        self.input_antiguo_nombre.grid(row=2, column=1)

        # Label del nombre nuevo
        self.nuevo_nombre = Label(
            frame_ep, text="Nombre Nuevo", font=("Calibri", 13))
        self.nuevo_nombre.grid(row=3, column=0)

        # Entry o input del nombre nuevo
        self.input_nuevo_nombre = Entry(frame_ep, font=("Calibri", 13))
        self.input_nuevo_nombre.grid(row=3, column=1)
        self.input_nuevo_nombre.focus()

        ##############   PRECIO  #########

        # Label del precio antiguo
        self.antiguo_precio = Label(
            frame_ep, text="Precio Antiguo", font=("Calibri", 13))
        self.antiguo_precio.grid(row=4, column=0)

        # Entry o input del precio antiguo
        self.input_antiguo_precio = Entry(frame_ep,
                                          textvariable=StringVar(
                                              self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Calibri", 13))
        self.input_antiguo_precio.grid(row=4, column=1)

        # Label del precio nuevo
        self.nuevo_precio = Label(
            frame_ep, text="Precio Nuevo", font=("Calibri", 13))
        self.nuevo_precio.grid(row=5, column=0)

        # Entry o input del precio nuevo
        self.input_nuevo_precio = Entry(frame_ep, font=("Calibri", 13))
        self.input_nuevo_precio.grid(row=5, column=1)

        #### categoría #####################

        # Label de categoría antigua
        self.antiguo_categoria = Label(
            frame_ep, text="Categoría antigua", font=("Calibri", 13))
        self.antiguo_categoria.grid(row=6, column=0)

        # Entry o input de antigua categoría
        self.input_antiguo_categoria = Entry(frame_ep,
                                             textvariable=StringVar(
                                                 self.ventana_editar, value=old_categoria),
                                             state="readonly", font=("Calibri", 13))
        self.input_antiguo_categoria.grid(row=6, column=1)

        # Label de nueva categoría
        self.nuevo_categoria = Label(
            frame_ep, text="Categoría nueva", font=("Calibri", 13))
        self.nuevo_categoria.grid(row=7, column=0)

        # Entry o input de la categoría nueva
        self.input_nuevo_categoria = Entry(frame_ep, font=("Calibri", 13))
        self.input_nuevo_categoria.grid(row=7, column=1)

        # boton actualizar producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=lambda:
                                           self.actualizar_productos(
                                               self.input_nuevo_nombre.get(),
                                               self.input_antiguo_nombre.get(),
                                               self.input_nuevo_precio.get(),
                                               self.input_antiguo_precio.get(),
                                               self.input_nuevo_categoria.get(),
                                               self.input_antiguo_categoria.get()
                                           ))

        self.boton_actualizar.grid(row=8, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nuevo_categoria,
                             antiguo_categoria):
        query = "UPDATE producto SET nombre=?,precio=?,categoria=? WHERE nombre=? AND precio=? AND categoria=?"
        parametros = (nuevo_nombre, nuevo_precio, nuevo_categoria,
                      antiguo_nombre, antiguo_precio, antiguo_categoria)
        self.db_consulta(query, parametros)
        self.ventana_editar.destroy()
        self.mensaje["text"] = "El producto  {} ha sido actualizado".format(
            antiguo_nombre)
        self.get_productos()


if __name__ == "__main__":
    root = Tk()  # root se da como nombre a la ventana principal
    app = Producto(root)
    root.mainloop()

    # prueba
