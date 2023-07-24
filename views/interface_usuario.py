# views/interface_usuario.py
import os
import tkinter as tk
from tkinter import messagebox
from models.produto import Produto
from models.estoque import Estoque

script_dir = os.path.dirname(os.path.abspath(__file__))

class InterfaceUsuario:
    def __init__(self, root, estoque, file_path):
        self.root = root
        self.estoque = estoque
        self.file_path = file_path

        
# Verifica se o arquivo de estoque existe
        if os.path.exists(self.file_path):
            # Caso exista, carrega o estoque a partir do arquivo
            self.estoque = Estoque(self.file_path)
        else:
            # Caso contrário, cria um novo estoque vazio
            self.estoque = Estoque()
            # E salva o estoque em um novo arquivo
            self.estoque.salvar_estoque(self.file_path)

        # Título
        self.label_titulo = tk.Label(root, text="Controle de Estoque", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=10)

        # Frame para os campos de entrada
        self.frame_entrada = tk.Frame(root)
        self.frame_entrada.pack(padx=20, pady=10)

        # Campos de entrada
        self.label_codigo = tk.Label(self.frame_entrada, text="Código de Barras:", font=("Arial", 12))
        self.label_codigo.grid(row=0, column=0, sticky=tk.W)
        self.entry_codigo = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entry_codigo.grid(row=0, column=1, padx=10)

        self.label_quantidade = tk.Label(self.frame_entrada, text="Quantidade:", font=("Arial", 12))
        self.label_quantidade.grid(row=1, column=0, sticky=tk.W)
        self.entry_quantidade = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.entry_quantidade.grid(row=1, column=1, padx=10)

        # Botões
        self.button_atualizar = tk.Button(root, text="Atualizar Estoque", font=("Arial", 12), command=self.atualizar_estoque)
        self.button_atualizar.pack(pady=10)

        self.button_verificar = tk.Button(root, text="Verificar Estoque", font=("Arial", 12), command=self.verificar_estoque_individual)
        self.button_verificar.pack(pady=10)

        self.button_verificar_minimo = tk.Button(root, text="Verificar Estoque Mínimo", font=("Arial", 12), command=self.verificar_estoque_minimo)
        self.button_verificar_minimo.pack(pady=10)

        self.button_gerar_planilha_minimo = tk.Button(root, text="Gerar Planilha Estoque Mínimo", font=("Arial", 12), command=self.gerar_planilha_estoque_minimo)
        self.button_gerar_planilha_minimo.pack(pady=10)
        self.button_cadastrar = tk.Button(root, text="Cadastrar Produto", font=("Arial", 12), command=self.cadastrar_produto)
        self.button_cadastrar.pack(pady=10)

        self.file_path = os.path.join(script_dir, "Estoque_com_codigo_de_barras.xlsx")
        self.estoque = Estoque(self.file_path)

    
    def cadastrar_produto(self):
        # Janela de diálogo para o cadastro do novo produto
        cadastrar_dialog = tk.Toplevel(self.root)
        cadastrar_dialog.title("Cadastrar Produto")
        cadastrar_dialog.geometry("400x300")

        # Campos de entrada para o cadastro do produto
        label_codigo = tk.Label(cadastrar_dialog, text="Código de Barras:", font=("Arial", 12))
        label_codigo.pack(pady=10)
        entry_codigo = tk.Entry(cadastrar_dialog, font=("Arial", 12), width=20)
        entry_codigo.pack()

        label_produto = tk.Label(cadastrar_dialog, text="Descrição do Produto:", font=("Arial", 12))
        label_produto.pack(pady=10)
        entry_produto = tk.Entry(cadastrar_dialog, font=("Arial", 12), width=30)
        entry_produto.pack()

        label_quantidade_atual = tk.Label(cadastrar_dialog, text="Quantidade Atual:", font=("Arial", 12))
        label_quantidade_atual.pack(pady=10)
        entry_quantidade_atual = tk.Entry(cadastrar_dialog, font=("Arial", 12), width=10)
        entry_quantidade_atual.pack()

        label_quantidade_minima = tk.Label(cadastrar_dialog, text="Quantidade Mínima:", font=("Arial", 12))
        label_quantidade_minima.pack(pady=10)
        entry_quantidade_minima = tk.Entry(cadastrar_dialog, font=("Arial", 12), width=10)
        entry_quantidade_minima.pack()
        
        def salvar_produto():
            codigo_barras = entry_codigo.get()
            produto_descricao = entry_produto.get()
            quantidade_atual = int(entry_quantidade_atual.get())
            quantidade_minima = int(entry_quantidade_minima.get())

            novo_produto = Produto(codigo_barras, quantidade_atual, quantidade_minima, produto=produto_descricao)
            self.estoque.produtos.append(novo_produto)
            self.estoque.salvar_estoque()
            messagebox.showinfo("Cadastrar Produto", "Produto cadastrado com sucesso!")
            cadastrar_dialog.destroy()
            
        button_salvar = tk.Button(cadastrar_dialog, text="Salvar", font=("Arial", 12), command=salvar_produto)
        button_salvar.pack(pady=10)
    
    
    def atualizar_estoque(self):
        codigo_barras = self.entry_codigo.get()
        quantidade = int(self.entry_quantidade.get())
        self.estoque.atualizar_produto(codigo_barras, quantidade)
        self.estoque.salvar_estoque()
        messagebox.showinfo("Atualização de Estoque", "Estoque atualizado com sucesso!")

    def verificar_estoque_individual(self):
        codigo_barras = self.entry_codigo.get()
        produto = self.estoque.verificar_estoque(codigo_barras=codigo_barras)

        if produto:
            mensagem = f"Informações do Produto:\n\n"
            mensagem += f"Código de Barras: {produto.codigo_barras}\n"
            mensagem += f"Descrição do Produto: {produto.produto}\n"
            mensagem += f"Quantidade em Estoque: {produto.quantidade_em_estoque}\n"
            mensagem += f"Quantidade Mínima: {produto.quantidade_minima}\n"
            mensagem += f"Entradas de Estoque: {produto.entrada_de_estoque}\n"
            mensagem += f"Saídas de Estoque: {produto.saida_de_estoque}\n"
            
            if produto.quantidade_em_estoque <= produto.quantidade_minima:
                mensagem += "\nEstoque abaixo do mínimo!"
            else:
                mensagem += "\nEstoque acima do mínimo!"
            
            messagebox.showinfo("Verificar Estoque", mensagem)
        else:
            messagebox.showinfo("Verificar Estoque", "Produto não encontrado no estoque!")

    def verificar_estoque_minimo(self):
        produtos_abaixo_minimo = self.estoque.verificar_estoque()
        if produtos_abaixo_minimo:
            mensagem = "Produtos abaixo do estoque mínimo:\n\n"
            for produto in produtos_abaixo_minimo:
                mensagem += str(produto) + "\n\n"
            messagebox.showinfo("Estoque Mínimo", mensagem)
        else:
            messagebox.showinfo("Estoque Mínimo", "Todos os produtos estão acima do estoque mínimo!")

    def gerar_planilha_estoque_minimo(self):
        self.estoque.gerar_planilha_estoque_minimo()
        
    
    def run(self):
        self.root.mainloop()