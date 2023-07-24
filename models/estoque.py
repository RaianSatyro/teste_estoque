import os
import pandas as pd
from models.produto import Produto
from tkinter import messagebox

class Estoque:
    def __init__(self, file_path):
        self.file_path = file_path
        self.produtos = self.carregar_estoque()



    def carregar_estoque(self):
        estoque_data = pd.read_excel(self.file_path)
        produtos = []
        for index, row in estoque_data.iterrows():
            produto = Produto(
                row['Codigo_de_Barras'],
                int(row['Quantidade_em_Estoque']),  # Converter para int
                int(row['Quantidade_Minima']),  # Converter para int
                produto=row.get('Produto', 'Produto Não Especificado')
            )
            produto.entrada_de_estoque = row.get('Entrada_de_Estoque', 0)
            produto.saida_de_estoque = row.get('Saida_de_Estoque', 0)
            produtos.append(produto)
        return produtos


    def salvar_estoque(self):
        data = {
            'Codigo_de_Barras': [produto.codigo_barras for produto in self.produtos],
            'Produto': [produto.produto for produto in self.produtos],  # Nova coluna para a descrição do produto
            'Quantidade_em_Estoque': [produto.quantidade_em_estoque for produto in self.produtos],
            'Quantidade_Minima': [produto.quantidade_minima for produto in self.produtos],
            'Entrada_de_Estoque': [produto.entrada_de_estoque for produto in self.produtos],
            'Saida_de_Estoque': [produto.saida_de_estoque for produto in self.produtos],
        }
        estoque_df = pd.DataFrame(data)
        estoque_df.to_excel(self.file_path, index=False)

    def atualizar_produto(self, codigo_barras, quantidade):
        for produto in self.produtos:
            if produto.codigo_barras == codigo_barras:
                produto.atualizar_estoque(quantidade)
                break

    def verificar_estoque(self, codigo_barras=None):
        if codigo_barras:
            for produto in self.produtos:
                if produto.codigo_barras == codigo_barras:
                    return produto
            return None
        else:
            return self.produtos
        
        
    def gerar_relatorio_estoque_minimo(self):
        produtos_abaixo_minimo = self.verificar_estoque()
        if produtos_abaixo_minimo:
            mensagem = "Produtos abaixo do estoque mínimo:\n\n"
            for produto in produtos_abaixo_minimo:
                mensagem += f"Código de Barras: {produto.codigo_barras}\n"
                mensagem += f"Descrição do Produto: {produto.produto}\n"
                mensagem += f"Quantidade em Estoque: {produto.quantidade_em_estoque}\n"
                mensagem += f"Quantidade Mínima: {produto.quantidade_minima}\n"
                mensagem += "------------------------\n"
            messagebox.showinfo("Estoque Mínimo", mensagem)
        else:
            messagebox.showinfo("Estoque Mínimo", "Todos os produtos estão acima do estoque mínimo!")

    def gerar_planilha_estoque_minimo(self):
        produtos_abaixo_minimo = self.verificar_estoque()
        if produtos_abaixo_minimo:
            data = {
                'Codigo_de_Barras': [produto.codigo_barras for produto in produtos_abaixo_minimo],
                'Quantidade_em_Estoque': [produto.quantidade_em_estoque for produto in produtos_abaixo_minimo],
                'Quantidade_Minima': [produto.quantidade_minima for produto in produtos_abaixo_minimo],
                'Entrada_de_Estoque': [produto.entrada_de_estoque for produto in produtos_abaixo_minimo],
                'Saida_de_Estoque': [produto.saida_de_estoque for produto in produtos_abaixo_minimo],
            }
            estoque_minimo_df = pd.DataFrame(data)
            estoque_minimo_df.to_excel('Estoque_Minimo.xlsx', index=False)
            messagebox.showinfo("Planilha Estoque Mínimo", "Planilha Estoque_Minimo.xlsx gerada com sucesso!")
        else:
            messagebox.showinfo("Planilha Estoque Mínimo", "Todos os produtos estão acima do estoque mínimo!")