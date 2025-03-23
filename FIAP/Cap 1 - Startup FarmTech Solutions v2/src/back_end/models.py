class Cultura:
    def __init__(self, nome, formato, dimensoes, area, insumo):
        self.nome = nome
        self.formato = formato
        self.dimensoes = dimensoes
        self.area = area
        self.insumo = insumo

class Insumo:
    def __init__(self, produto, dose, quantidade, extras=None):
        self.produto = produto
        self.dose = dose
        self.quantidade = quantidade
        self.extras = extras
