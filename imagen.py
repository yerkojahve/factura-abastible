import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ConvertidorICOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor de Imagen a ICO")
        
        # Crear el botón para seleccionar el archivo
        self.boton_seleccionar = tk.Button(root, text="Seleccionar Imagen", command=self.seleccionar_imagen)
        self.boton_seleccionar.pack(pady=20)
        
    def seleccionar_imagen(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo JPG o PNG
        ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        
        if ruta_imagen:
            # Abrir la imagen con Pillow
            imagen = Image.open(ruta_imagen)
            
            # Convertir la imagen a ícono (ICO)
            ruta_ico = ruta_imagen.rsplit(".", 1)[0] + ".ico"
            imagen.save(ruta_ico, format="ICO")
            
            # Mostrar un mensaje de éxito
            mensaje = f"La imagen se convirtió a ícono y se guardó como '{ruta_ico}'"
            tk.messagebox.showinfo("Éxito", mensaje)

# Crear la ventana principal
root = tk.Tk()
app = ConvertidorICOApp(root)
root.mainloop()