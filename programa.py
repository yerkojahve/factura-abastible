import tkinter as tk
from tkinter import ttk, filedialog
import mysql.connector 
from tkinter import messagebox
from db import connection, guardar_datos_en_db, obtener_id_cliente, buscar_cliente_por_id
from tkinter import simpledialog
from tkcalendar import Calendar
from PyPDF2 import PdfReader
import pdf,os, time, re
from PIL import Image, ImageTk
from web import iniciar_facturar, iniciar_despacho


pad10 = {"padx": 5, "pady": 5}

int = int
ipad10 = {"ipadx": 8, "ipady": 8}

boton_estilo = {
            'bg': '#003594',  # Fondo azul
            'fg': 'white',    # Texto blanco
            'font': ('Arial', 12),
        }

estilo_label = {
    "foreground": "white",  # Color del texto
    "font": ("Arial", 10, "bold"),  # Fuente y tamaño del texto
    "background": "#ff6900"  # Color de fondo del Label
}





class App:
    def __init__(self, root):

        self.root = root
        
        self.root.title("Facturas")
        self.root.geometry('800x600')
        self.root.iconbitmap('img/ABASTIBLE.ico')
        self.style = ttk.Style()
        
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Clientes")
        self.set_background(self.tab1, "img/bg-naranja.png")       
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Factura")
        self.set_background(self.tab2, "img/bg-naranja.png")  

        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Conductor")
        self.set_background(self.tab3, "img/bg-naranja.png")  
        
        self.notebook.bind("<<NotebookTabChanged>>", self.actualizar_contenido)


        self.datos_cliente_aux = {
            'idCliente': None,
            'Nombre': None,
            'Rut': None,
            'dv': None,
            'Conductor': None,
            'Telefono': None,
            'TipoCliente': None,
            'factura':{
                'rut_comercio':None,
            }
        }
        
        self.style.configure('EstiloBoton.TButton', 
                              background='#003594',  # Fondo azul
                              foreground='white',     # Texto blanco
                              font=('Arial', 12))

        self.configurar_estilos()
        self.configurar_pestaña1()
        self.configurar_pestaña2()

    def set_rut(self, rut, verificador):
        self.datos_cliente_aux['Rut'] = rut
        self.datos_cliente_aux['dv'] = verificador
    
    def get_rut(self):
        return self.datos_cliente_aux['Rut']
    
    def get_dv(self):
        return self.datos_cliente_aux["dv"]
    
    def set_nombre(self, nombre):
        self.datos_cliente_aux['Nombre'] = nombre
    
    def get_nombre(self):
        return self.datos_cliente_aux['Nombre']
    
    def set_background(self, tab, image_path):
        # Carga la imagen y conviértela en un objeto ImageTk
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        
        # Crea un widget Label para mostrar la imagen en el fondo de la pestaña
        background_label = tk.Label(tab, image=photo)
        background_label.image = photo  # Evita que la imagen sea eliminada por el recolector de basura
        background_label.place(relwidth=1, relheight=1)
    
    def configurar_estilos(self):

        self.style.configure("naranjo.TFrame", background='#ff6900')
        self.style.configure("celeste.TFrame", background='#87CEEB')
        self.style.configure("TFrame.Colored", background='#ff6900')
        self.style.configure("Label.WhiteText.TLabel", foreground="white", font=("Arial", 14, "bold"), background="#ff6900")
        self.style.configure("TCombobox", fieldbackground="#ff6900", borderwidth=2)

    def configurar_pestaña1(self):

        main_frame = ttk.Frame(self.tab1,style="naranjo.TFrame" ,borderwidth=2)
        main_frame.pack()

        frame2 = ttk.Frame(self.tab1, style="naranjo.TFrame", borderwidth=2, relief="solid")
        frame2.pack()

        def crear_label_y_entry(row, text):
            label = tk.Label(main_frame,**estilo_label, text=text, )
            label.grid(row=row, column=0, padx=10, pady=5)
            entry = tk.Entry(main_frame, )
            entry.grid(row=row, column=1, padx=10, pady=5)
            return label, entry

        self.label_rut, self.entry_rut = crear_label_y_entry(0, "RUT:")
        self.label_nombre, self.entry_nombre = crear_label_y_entry(1, "Nombre:")
        self.label_conductor, self.entry_conductor = crear_label_y_entry(2, "Conductor:")

        self.button_guardar = tk.Button(main_frame, text="Guardar",**boton_estilo, command=self.guardar_usuario)
        self.button_guardar.grid(row=0, column=2, **pad10, **ipad10)

        self.button_borrar = tk.Button(main_frame, text="Borrar",**boton_estilo,  command=self.borrar_usuario)
        self.button_borrar.grid(row=1, column=2, **pad10, **ipad10)

        self.boton_limpiar = tk.Button(main_frame, text="Limpiar",**boton_estilo,  command=self.limpiar_casillas)
        self.boton_limpiar.grid(row=2, column=2, **pad10, **ipad10)

        # Agregar un Combobox para buscar por nombre
        self.combobox_nombres = ttk.Combobox(frame2)
        self.combobox_nombres.grid(row=5, column=1, padx=10, pady=5)

        self.combobox_nombres.bind("<KeyRelease>", self.actualizar_combobox)

        self.label_commbobox = ttk.Label(frame2,style="Label.WhiteText.TLabel", text="Busqueda")
        self.label_commbobox.grid(row=5, column=0, padx=10, pady=5)

        self.tree = ttk.Treeview(frame2, columns=("RUT", "Nombre", "Conductor"), show="headings")
        self.tree.heading("RUT", text="RUT")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Conductor", text="Conductor")

        # Configurar un Scrollbar vertical
        y_scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=y_scrollbar.set)

        # Colocar el Treeview y el Scrollbar en el frame
        self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=5)
        y_scrollbar.grid(row=7, column=4, sticky="ns")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tree.bind("<Double-1>", self.abrir_ventana_edicion)

        self.button_actualizar = tk.Button(frame2, text="Actualizar", **boton_estilo, command=self.actualizar_tabla)
        self.button_actualizar.grid(row=8, column=0, columnspan=4, padx=10, pady=5)

        self.datos_seleccionados = {"rut": "", "nombre": "", "conductor": ""}

    def actualizar_contenido(self, event):
        current_tab = self.notebook.tabs()[self.notebook.index("current")]
        if current_tab == self.tab1:
            self.tab2.pack_forget()
            self.tab1.pack()
        elif current_tab == self.tab2:
            self.tab1.pack_forget()
            self.tab2.pack()

    def guardar_usuario(self):

        rut = self.entry_rut.get()
        nombre = self.entry_nombre.get()
        conductor = self.entry_conductor.get()

        print(rut)

        if self.validar_rut(rut):
            cursor = connection.cursor()

            query = "INSERT INTO cliente (Rut, Nombre, Conductor) VALUES (%s, %s, %s)"
            values = (rut, nombre,conductor)
            cursor.execute(query, values)

            connection.commit()
        else:
            self.mostrar_mensaje("rut invalido siga formato")
        
    def borrar_usuario(self):
        nombre = self.entry_nombre.get()

        cursor = connection.cursor()

        query = "DELETE FROM cliente WHERE nombre = %s"
        values = (nombre,)
        cursor.execute(query, values)

        connection.commit()
        
        cursor.close()
        self.actualizar_tabla
        self.mostrar_mensaje("Usuario borrado correctamente")
        self.limpiar_casillas()
         
    def limpiar_casillas(self):
        self.entry_rut.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_conductor.delete(0, "end")

    """def obtener_datos_usuario(self, event=None):
            rut = self.entry_rut.get()
            nombre = self.entry_nombre.get()
            conductor = self.entry_conductor.get()

            # Realizar la búsqueda en la base de datos
            cursor = connection.cursor()

            # Define la consulta SQL en función de los campos completados
            if rut:
                query = "SELECT nombre, Conductor FROM cliente WHERE rut = %s"
                values = (rut,)
            elif nombre:
                query = "SELECT rut, Conductor FROM cliente WHERE nombre = %s"
                values = (nombre,)
            elif conductor:
                query = "SELECT rut, nombre FROM cliente WHERE Conductor = %s"
                values = (conductor,)
            else:
                return  # No hay campos completados

            cursor.execute(query, values)
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                if len(resultados) == 1:
                    # Rellenar los campos con el resultado único
                    resultado = resultados[0]
                    if rut:
                        self.entry_nombre.delete(0, tk.END)
                        self.entry_nombre.insert(0, resultado[0])
                        self.entry_conductor.delete(0, tk.END)
                        self.entry_conductor.insert(0, resultado[1])
                    elif nombre:
                        self.entry_rut.delete(0, tk.END)
                        self.entry_rut.insert(0, resultado[0])
                        self.entry_conductor.delete(0, tk.END)
                        self.entry_conductor.insert(0, resultado[1])
                    elif conductor:
                        self.entry_rut.delete(0, tk.END)
                        self.entry_rut.insert(0, resultado[0])
                        self.entry_nombre.delete(0, tk.END)
                        self.entry_nombre.insert(0, resultado[1])
                else:
                    # Mostrar una lista de resultados en una ventana emergente
                    seleccion = simpledialog.askstring("Resultados", "Se encontraron múltiples resultados con el mismo nombre:\n\n" + "\n".join([f"{r[0]}, {r[1]}" for r in resultados]) + "\n\nPor favor, seleccione el RUT de la persona deseada:")
                    if seleccion:
                        self.entry_rut.delete(0, tk.END)
                        self.entry_rut.insert(0, seleccion)"""
    
    def abrir_ventana_edicion(self, event):
        item = self.tree.selection()[0]  # Obtener el índice de la fila seleccionada
        rut = self.tree.item(item, "values")[0]  # Obtener el valor de la columna RUT
        nombre = self.tree.item(item, "values")[1]  # Obtener el valor de la columna Nombre
        conductor = self.tree.item(item, "values")[2]  # Obtener el valor de la columna Conductor

        # Crear una nueva ventana de edición
        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar Usuario")
        ventana_edicion.geometry("400x300")

        # Crear casillas de entrada para editar los datos
        tk.Label(ventana_edicion, text="RUT:").pack()
        entry_rut = tk.Entry(ventana_edicion)
        entry_rut.pack()
        entry_rut.insert(0, rut)

        tk.Label(ventana_edicion, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_edicion)
        entry_nombre.pack()
        entry_nombre.insert(0, nombre)

        tk.Label(ventana_edicion, text="Conductor:").pack()
        entry_conductor = tk.Entry(ventana_edicion)
        entry_conductor.pack()
        entry_conductor.insert(0, conductor)

        # Función para guardar cambios en la base de datos
        def guardar_cambios():
            nuevo_rut = entry_rut.get()
            nuevo_nombre = entry_nombre.get()
            nuevo_conductor = entry_conductor.get()

            cursor = connection.cursor()

            # Sentencia SQL de actualización
            query = "UPDATE cliente SET Nombre = %s, Conductor = %s WHERE Rut = %s"
            values = (nuevo_nombre, nuevo_conductor, nuevo_rut)

            try:
                cursor.execute(query, values)
                connection.commit()
                print("Datos actualizados correctamente")
            except mysql.connector.Error as err:
                print(f"Error al actualizar datos: {err}")

            cursor.close()

        # Botón para guardar cambios
        btn_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.pack()

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Mensaje", mensaje)

    def buscar_persona(self):
        nombre_a_buscar = self.combobox_nombres.get()

        cursor = connection.cursor()

        query = "SELECT rut, nombre FROM cliente WHERE nombre = %s"
        values = (nombre_a_buscar,)
        cursor.execute(query, values)
        resultados = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())

        for resultado in resultados:
            self.tree.insert("", "end", values=(resultado[0], resultado[1]))

    
        cursor.close() 

    def actualizar_combobox(self, event):
        texto_busqueda = self.combobox_nombres.get()

        cursor = connection.cursor()

        query = "SELECT RUT, Nombre, Conductor FROM cliente WHERE RUT LIKE %s OR Nombre LIKE %s OR Conductor LIKE %s"
        values = (f"%{texto_busqueda}%", f"%{texto_busqueda}%", f"%{texto_busqueda}%")
        cursor.execute(query, values)
        resultados = cursor.fetchall()

        # Limpiar la tabla antes de agregar los resultados actualizados
        self.tree.delete(*self.tree.get_children())

        for resultado in resultados:
            # Insertar cada fila de resultado en el Treeview
            self.tree.insert("", "end", values=resultado)

        cursor.close()

    def seleccionar_nombre(self, event):
        # Obtener el nombre seleccionado en el Listbox
        seleccion = self.lista_nombres.get(self.lista_nombres.curselection())

        # Dividir el nombre y el conductor
        nombre, conductor = seleccion.split(" - ")

        # Llenar los campos correspondientes
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)
        self.entry_conductor.delete(0, tk.END)
        self.entry_conductor.insert(0, conductor)

    def seleccionar_fila(self, event):
        item = self.tree.selection()[0]  # Obtener el índice de la fila seleccionada
        values = self.tree.item(item, "values")

        # Inicializar las variables con valores por defecto en caso de que no existan en la tupla
        rut = ""
        nombre = ""
        conductor = ""

        if values:
            if len(values) > 0:
                rut = values[0]
            if len(values) > 1:
                nombre = values[1]
            if len(values) > 2:
                conductor = values[2]

        # Actualizar las casillas de entrada en la pestaña actual
        if self.root.nametowidget(self.notebook.select()) == self.tab1:
            self.entry_rut.delete(0, "end")
            self.entry_rut.insert(0, rut)

            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, nombre)

            self.entry_conductor.delete(0, "end")
            self.entry_conductor.insert(0, conductor)

            # Actualizar la variable de datos seleccionados si es necesario
            self.datos_seleccionados["rut"] = rut
            self.datos_seleccionados["nombre"] = nombre
            self.datos_seleccionados["conductor"] = conductor
        else:
            # Si estás en otra pestaña, actualiza las casillas de entrada en esa pestaña
            # Aquí deberías manejar la lógica según la estructura de la pestaña en la que te encuentras
            # Puedes agregar más condiciones según sea necesario
            pass

    def actualizar_tabla(self):
        cursor = connection.cursor()

        query = "SELECT rut, nombre, Conductor FROM cliente"
        cursor.execute(query)
        usuarios = cursor.fetchall()

        # Limpiar la tabla antes de actualizar
        self.tree.delete(*self.tree.get_children())

        for usuario in usuarios:
            self.tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))

        cursor.close()
        self.mostrar_mensaje("Tabla actualizada")

     #---- METODOS PESTAÑA 2 ----- 
    
    def validar_rut(self, entry_text):
        # Define la expresión regular para el formato de RUT
        rut_pattern = r'^\d{7,8}-[\dkK]$'

        # Comprueba si el texto coincide con la expresión regular
        if re.match(rut_pattern, entry_text):
            return True
        else:
            return False

    def configurar_pestaña2(self):

        main_frame = ttk.Frame(self.tab2, style="naranjo.TFrame", borderwidth=5)  # Aumentar el grosor del borde
        main_frame.pack(padx=20, pady=20)

        # Combobox de clientes
        self.combobox_clientes = ttk.Combobox(main_frame, width=50)  # Aumentar el ancho del Combobox
        self.combobox_clientes.grid(row=0, column=1, padx=10, pady=10, sticky='w')  # Alineación izquierda
        # Cargar los nombres de los clientes desde la base de datos
        self.cargar_clientes()

        self.combobox_clientes.bind("<<ComboboxSelected>>", self.seleccionar_cliente)

        self.clientes = self.configurar_combobox()

        # Etiqueta "Cliente"
        self.label_cliente = ttk.Label(main_frame, **estilo_label, text="Cliente:")
        self.label_cliente.grid(row=0, column=0, padx=10, pady=10, sticky='w')  # Alineación izquierda
        
        # Vincula la función 'seleccionar_cliente' al evento del combobox
        self.combobox_clientes.bind("<<ComboboxSelected>>", self.seleccionar_cliente)
        
        # Etiqueta y entrada para "Producto Nombre"
        ttk.Label(main_frame, **estilo_label, text="Producto Nombre:").grid(row=4, column=0, padx=10, pady=10, sticky='w')  # Alineación izquierda
        entry_producto_nombre = ttk.Entry(main_frame, width=50)  # Aumentar el ancho de la entrada
        entry_producto_nombre.grid(row=4, column=1, padx=10, pady=10, sticky='w')  # Alineación izquierda

        # Etiqueta y entrada para "Cantidad"
        ttk.Label(main_frame, **estilo_label, text="Cantidad:").grid(row=5, column=0, padx=10, pady=10, sticky='w')

        # Spinbox para la entrada de cantidad
        cantidad_var = tk.StringVar()
        cantidad_spinbox = tk.Spinbox(main_frame, from_=0, to=1000, textvariable=cantidad_var, width=10)  # Puedes ajustar los valores de 'from_' y 'to' según tus necesidades
        cantidad_spinbox.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Etiqueta y entrada para "Precio Porcentaje"
        ttk.Label(main_frame, **estilo_label, text="Precio Porcentaje:").grid(row=7, column=0, padx=10, pady=10, sticky='w')  # Alineación izquierda
        entry_precio = ttk.Entry(main_frame, width=50)  # Aumentar el ancho de la entrada
        entry_precio.grid(row=7, column=1, padx=10, pady=10, sticky='w')  # Alineación izquierda

        # Checkbox "Incluir Descripción"
        self.incluir_descripcion = tk.BooleanVar()
        descripcion_checkbox = tk.Checkbutton(main_frame, **estilo_label, text="Incluir Descripción", variable=self.incluir_descripcion, command=self.toggle_descripcion)
        descripcion_checkbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='w')  # Alineación izquierda


         # Etiqueta y entrada para "Descripción"
        ttk.Label(main_frame, **estilo_label, text="Descripción:").grid(row=9, column=0, padx=10, pady=10, sticky='w')  # Alineación izquierda
        self.descripcion_var = tk.StringVar()  
        self.entry_descripcion = ttk.Entry(main_frame, textvariable=self.descripcion_var, width=50)  # Aumentar el ancho de la entrada
        self.entry_descripcion.grid(row=9, column=1, padx=10, pady=10, sticky='w')  # Alineación izquierda
        
        # Botón para iniciar sesión
        ttk.Button(main_frame, text="Facturar", command=lambda: iniciar_facturar(
            self.get_rut(), self.get_dv(),
            entry_producto_nombre.get(), cantidad_var.get(),
            entry_precio.get(), self.descripcion_var.get() if self.incluir_descripcion.get() else None
        )).grid(row=11, column=0, columnspan=1, pady=20)

        ttk.Button(main_frame, text="Despacho", command=lambda: iniciar_despacho(
            self.get_rut(), self.get_dv(),
            entry_producto_nombre.get(), cantidad_var.get(),
            entry_precio.get(), self.descripcion_var.get() if self.incluir_descripcion.get() else None
        )).grid(row=11, column=1, columnspan=1, pady=20)

        #self.boton_cargar_pdf = ttk.Button(main_frame, text="Cargar PDF", command=self.cargar_pdf)
        #self.boton_cargar_pdf.grid(row=13, column=0, columnspan=2, **pad10)

        #self.boton_crear_factura = ttk.Button(main_frame, text="Crear Factura ", command=self.ventana_crear_factura)
        #self.boton_crear_factura.grid(row=14, column=0, columnspan=2, **pad10)
    
    def agregar_factura(self):
        cliente_seleccionado = self.combobox_clientes.get()
        fecha_factura = self.entry_fecha_factura.get()
        monto_factura = self.entry_monto_factura.get()
        rut_comercio = self.entry_rutcomercio.get()

        # Validar los campos antes de agregar la factura
        if not cliente_seleccionado or not fecha_factura or not monto_factura or not rut_comercio:
            self.mostrar_mensaje("Complete todos los campos para agregar la factura.")
            return

        try:
            cursor = connection.cursor()

            # Insertar la factura en la tabla de facturas con el "rut_comercio"
            query_insertar_factura = "INSERT INTO factura (Fecha, Monto, rut_comercio) VALUES (%s, %s, %s)"
            cursor.execute(query_insertar_factura, (fecha_factura, monto_factura, rut_comercio))
            connection.commit()

            cursor.close()

            self.mostrar_mensaje("La factura se ha agregado correctamente.")
        except mysql.connector.Error as err:
            self.mostrar_mensaje(f"Error al agregar la factura: {err}")

    def cargar_clientes(self):
        cursor = connection.cursor()

        # Consulta SQL para obtener los nombres de los clientes y sus IDs
        query = "SELECT IdCliente, Nombre FROM cliente"
        cursor.execute(query)

        # Obtener los nombres de los clientes y almacenar sus IDs en un diccionario
        clientes = {}
        for row in cursor.fetchall():
            id_cliente, nombre_cliente = row
            clientes[nombre_cliente] = id_cliente

        # Cargar los nombres de los clientes en el combobox
        self.combobox_clientes['values'] = list(clientes.keys())

        self.datos_cliente = None
        self.cliente_seleccionado = None  

        # Cuando se seleccione un cliente en el combobox, almacenar su ID
        def seleccionar_cliente(event):
            
            cliente_seleccionado = self.combobox_clientes.get()
            self.id_cliente_seleccionado = clientes.get(cliente_seleccionado)
            if self.id_cliente_seleccionado is not None:
                datos_cliente = buscar_cliente_por_id(self.id_cliente_seleccionado)
                if datos_cliente:
                    # Almacena datos_cliente como un atributo de la instancia de la clase
                    self.datos_cliente = datos_cliente
                    self.cliente_seleccionado = cliente_seleccionado
                    return (self.datos_cliente,self.cliente_seleccionado)
                else:
                    print("Cliente no encontrado")
                    return None, None
            else:
                print("Cliente no encontrado")
                return None, None
        
        self.combobox_clientes.bind("<<ComboboxSelected>>", seleccionar_cliente)
    
    def configurar_combobox(self):
        cursor = connection.cursor()

        # Consulta SQL para obtener los nombres de los clientes y sus IDs
        query = "SELECT IdCliente, Nombre FROM cliente"
        cursor.execute(query)

        # Obtener los nombres de los clientes y almacenar sus IDs en un diccionario
        clientes = {}
        for row in cursor.fetchall():
            id_cliente, nombre_cliente = row
            clientes[nombre_cliente] = id_cliente

        # Cargar los nombres de los clientes en el combobox
        self.combobox_clientes['values'] = list(clientes.keys())

        return clientes
    
    def seleccionar_cliente(self, event):
        cliente_seleccionado = self.combobox_clientes.get()
        id_cliente_seleccionado = self.clientes.get(cliente_seleccionado)
        if id_cliente_seleccionado is not None:
            datos_cliente = buscar_cliente_por_id(id_cliente_seleccionado)
            if datos_cliente:
                self.datos_cliente_aux['Nombre'] = datos_cliente['Nombre']
                self.datos_cliente_aux['Rut'] = datos_cliente['Rut']
                rut_completo = self.datos_cliente_aux.get('Rut', '')
                rut, verificador = self.dividir_rut(rut_completo)
                self.datos_cliente_aux['Rut'] = rut
                self.datos_cliente_aux['dv']= verificador
                self.cliente_seleccionado = cliente_seleccionado
                print(self.get_dv())
                print(self.get_rut())
            else:
                print("Cliente no encontrado")
        else:
            print("Cliente no encontrado")

    def obtener_fecha(self):
        fecha_seleccionada = self.date_picker.get_date()
        print(f"Fecha seleccionada: {fecha_seleccionada}")
        self.entry_fecha_factura.delete(0, tk.END)
        self.entry_fecha_factura.insert(0,fecha_seleccionada)
    
    def cargar_pdf(self):
        # Abre el diálogo de selección de archivo
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        if file_path:
            try:
                # Abre el archivo PDF
                pdf_reader = PdfReader(file_path)

                # Inicializa una cadena para almacenar todo el texto del PDF
                texto_completo = ""

                # Recorre cada página del PDF y extrae su texto
                for page in pdf_reader.pages:
                    texto_completo += page.extract_text()

                # Extraer información desde el texto extraído
                vector_datos = pdf.extraer_informacion_desde_texto(texto_completo)
                print(vector_datos)
                # Accede al valor de 'rut_cliente' desde el diccionario
                rut_cliente = vector_datos['rut_cliente']
                print(f'RUT del cliente: {rut_cliente}')

                # Consultar la base de datos para obtener el ID del cliente
                id_cliente = obtener_id_cliente(rut_cliente)

                if id_cliente is not None:
                    print(f'ID del cliente: {id_cliente}')
                    # Asocia el ID del cliente al dato de la factura
                    vector_datos['idCliente'] = id_cliente

                guardar_datos_en_db(vector_datos,id_cliente)

                return vector_datos
            except Exception as e:
                self.mostrar_mensaje(f"Error al cargar el PDF: {str(e)}")

        # Si no se selecciona ningún archivo o ocurre un error, retornar None
        return None

    def guardar_datos(self):
        # Obtener los datos ingresados
        nombre_cliente = self.entry_nombre.get()
        rut_cliente = self.entry_rut.get()
        numero_factura = self.entry_numero_factura.get()
        monto_total = self.entry_monto_total.get()

        try:
            cursor = connection.cursor()

            # Iniciar una transacción
            cursor.execute("START TRANSACTION")

            # Insertar datos en la tabla "cliente"
            query_insertar_cliente = "INSERT INTO cliente (Nombre, Rut) VALUES (%s, %s)"
            valores_cliente = (nombre_cliente, rut_cliente)
            cursor.execute(query_insertar_cliente, valores_cliente)

            # Obtener el ID del cliente recién insertado
            id_cliente = cursor.lastrowid

            # Insertar datos en la tabla "factura"
            query_insertar_factura = "INSERT INTO factura (numero_factura, idCliente, monto) VALUES (%s, %s, %s)"
            valores_factura = (numero_factura, id_cliente, monto_total)
            cursor.execute(query_insertar_factura, valores_factura)

            # Confirmar la transacción
            cursor.execute("COMMIT")

            # Cerrar el cursor
            cursor.close()

            # Limpiar los campos de entrada
            self.entry_nombre.delete(0, tk.END)
            self.entry_rut.delete(0, tk.END)
            self.entry_numero_factura.delete(0, tk.END)
            self.entry_monto_total.delete(0, tk.END)

            # Mostrar un mensaje de éxito
            self.mostrar_mensaje("Tabla actualizada")


        except mysql.connector.Error as err:
            # Si ocurre un error, deshacer la transacción
            cursor.execute("ROLLBACK")

            # Mostrar un mensaje de error
            self.mostrar_mensaje(f"Error al guardar los datos: {err}")
        
    def ventana_crear_factura(self):

        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar Usuario")
        ventana_edicion.geometry("900x700")

        ttk.Label(ventana_edicion, text="Cliente:").grid(row=0, column=0, **pad10)
        self.combobox_clientes = ttk.Combobox(ventana_edicion)
        self.combobox_clientes.grid(row=0, column=1, **pad10)
        
        # Label y Entry para el Rut del Comercio
        ttk.Label(ventana_edicion, text="Rut Comercio:").grid(row=1, column=0, **pad10)
        self.entry_rutcomercio = ttk.Entry(ventana_edicion)
        self.entry_rutcomercio.grid(row=1, column=1, **pad10)

        # Cargar los nombres de los clientes desde la base de datos
        self.cargar_clientes()

        # Label y Entry para la Fecha de la Factura
        ttk.Label(ventana_edicion, text="Fecha de la Factura:").grid(row=2, column=0, **pad10)
        self.entry_fecha_factura = ttk.Entry(ventana_edicion)
        self.entry_fecha_factura.grid(row=2, column=1, **pad10)

        # Label y Entry para el Monto de la Factura
        ttk.Label(ventana_edicion, text="Monto de la Factura:").grid(row=3, column=0, **pad10)
        self.entry_monto_factura = ttk.Entry(ventana_edicion)
        self.entry_monto_factura.grid(row=3, column=1, **pad10)

        # Botón para agregar la factura
        ttk.Button(ventana_edicion, text="Agregar Factura", command=self.agregar_factura).grid(row=8, column=0, columnspan=2, **pad10)

        # Widget de calendario en lugar de un Entry para la Fecha de la Factura
        self.date_picker = Calendar(ventana_edicion)
        self.date_picker.grid(row=6, column=1, padx=10, pady=10)

        # Label y Entry para el Nombre del Cliente
        tk.Label(ventana_edicion, text="Nombre Cliente:").grid(row=0, column=2, **pad10)
        self.entry_nombre_cliente = tk.Entry(ventana_edicion)
        self.entry_nombre_cliente.grid(row=0, column=3, **pad10)

        # Label y Entry para el RUT del Cliente
        tk.Label(ventana_edicion, text="RUT Cliente:").grid(row=1, column=2, **pad10)
        self.entry_rut_cliente = tk.Entry(ventana_edicion)
        self.entry_rut_cliente.grid(row=1, column=3, **pad10)

        # Label y Entry para el Número de Factura
        tk.Label(ventana_edicion, text="Número de Factura:").grid(row=1, column=4, **pad10)
        self.entry_numero_factura = tk.Entry(ventana_edicion)
        self.entry_numero_factura.grid(row=1, column=5, **pad10)

        # Label y Entry para el Monto Total
        tk.Label(ventana_edicion, text="Monto Total:").grid(row=2, column=4, **pad10)
        self.entry_monto_total = tk.Entry(ventana_edicion)
        self.entry_monto_total.grid(row=2, column=5, **pad10)

        # Botón para guardar los datos
        tk.Button(ventana_edicion, text="Guardar Datos", command=self.guardar_datos).grid(row=3, column=3, **pad10)
    
    def abrir_ventana_agregar_datos_sii(self):

        ventana = tk.Toplevel()
        ventana.title("Iniciar Sesión en SII")
        ventana.geometry("400x700")
    
        self.clientes = self.configurar_combobox()

        self.label_cliente = ttk.Label(ventana, text="Cliente:")
        self.label_cliente.grid(row=0, column=0, **pad10)
        
        self.combobox_clientes = ttk.Combobox(ventana, values=list(self.clientes.keys()))
        self.combobox_clientes.grid(row=0, column=1, **pad10)

        # Vincula la función 'seleccionar_cliente' al evento del combobox
        self.combobox_clientes.bind("<<ComboboxSelected>>", self.seleccionar_cliente)
        
        ttk.Label(ventana, text="Producto Nombre:").grid(row=4, column=0, padx=10, pady=10)
        entry_producto_nombre = ttk.Entry(ventana)
        entry_producto_nombre.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(ventana, text="Cantidad:").grid(row=5, column=0, padx=10, pady=10)
        entry_cantidad = ttk.Entry(ventana)
        entry_cantidad.grid(row=5, column=1, padx=10, pady=10)

        ttk.Label(ventana, text="Precio:").grid(row=7, column=0, padx=10, pady=10)
        entry_precio = ttk.Entry(ventana)
        entry_precio.grid(row=7, column=1, padx=10, pady=10)

        self.incluir_descripcion = tk.BooleanVar()

        self.incluir_descripcion = tk.BooleanVar()

        # Crear el checkbox
        descripcion_checkbox = tk.Checkbutton(ventana, text="Incluir Descripción", variable=self.incluir_descripcion, command=self.toggle_descripcion)
        descripcion_checkbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Etiqueta y entrada para la descripción (creada dinámicamente solo si el checkbox está marcado)
        self.descripcion_var = tk.StringVar()  # Variable para almacenar el contenido de la entrada
        self.entry_descripcion = ttk.Entry(ventana, textvariable=self.descripcion_var)
        self.entry_descripcion.grid(row=9, column=0,columnspan=2, padx=10, pady=10)

        
        # Botón para iniciar sesión
        ttk.Button(ventana, text="Factura", command=lambda: iniciar_facturar(
            self.get_rut(), self.get_dv(),
            entry_producto_nombre.get(), entry_cantidad.get(),
            entry_precio.get(), self.descripcion_var.get() if self.incluir_descripcion.get() else None , True
        )).grid(row=11, column=0, columnspan=0, pady=20)

        ttk.Button(ventana, text="Guia Despacho", command=lambda: iniciar_despacho(
            self.get_rut(), self.get_dv(),
            entry_producto_nombre.get(), entry_cantidad.get(),
            entry_precio.get(), self.descripcion_var.get() if self.incluir_descripcion.get() else None, False
        )).grid(row=12, column=1, columnspan=0, pady=20)

    def mostrar_estado(self):
        self.style('EstiloBoton.TButton', 
                 background='#003594',  # Fondo azul
                 foreground='white',     # Texto blanco
                 font=('Arial', 12))
    
    def toggle_descripcion(self):
        if self.incluir_descripcion.get():
            self.entry_descripcion.grid()  # Mostrar la casilla si el checkbox está marcado
        else:
            self.entry_descripcion.grid_remove()

    def dividir_rut(self, rut_completo):
        rut, verificador = rut_completo.split('-')
        return rut, verificador

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
