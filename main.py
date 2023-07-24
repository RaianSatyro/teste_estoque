import os
import tkinter as tk
from models.estoque import Estoque
from views.interface_usuario import InterfaceUsuario

file_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(file_dir, "data")
file_path = os.path.join(data_dir, "Estoque_com_codigo_de_barras.xlsx")
estoque = Estoque(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    interface = InterfaceUsuario(root, estoque, file_path)
    interface.run()
