

class Produto:
    def __init__(self, codigo_barras, quantidade_em_estoque, quantidade_minima, produto="Produto Não Especificado"):
        self.codigo_barras = codigo_barras
        self.produto = produto
        self.quantidade_em_estoque = quantidade_em_estoque
        self.quantidade_minima = quantidade_minima
        self.entrada_de_estoque = 0
        self.saida_de_estoque = 0


    def atualizar_estoque(self, quantidade):
        if quantidade >= 0:
            self.quantidade_em_estoque += quantidade
            self.entrada_de_estoque += quantidade
        else:
            self.quantidade_em_estoque += quantidade
            self.saida_de_estoque += abs(quantidade)

        if self.quantidade_em_estoque <= self.quantidade_minima:
            print("Estoque baixo para o produto:", self.produto)

    def __str__(self):
        return f"Codigo de Barras: {self.codigo_barras}, Produto: {self.produto}, Quantidade em Estoque: {self.quantidade_em_estoque}"