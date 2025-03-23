class Cultura:
    def __init__(self, cultura, formato, dimensoes, area, insumo):
        self.cultura = cultura
        self.formato = formato
        self.dimensoes = dimensoes
        self.area = area
        self.insumo = insumo

    def to_dict(self):
        return {
            "cultura": self.cultura,
            "formato": self.formato,
            "dimensoes": self.dimensoes,
            "area": self.area,
            "insumo": self.insumo.to_dict()
        }
class Insumo:
    def __init__(self, produto, dose, quantidade, extras=None):
        self.produto = produto
        self.dose = dose
        self.quantidade = quantidade
        self.extras = extras

    def to_dict(self):
        return {
            "produto": self.produto,
            "dose": self.dose,
            "quantidade": self.quantidade,
            "extras": self.extras
        }

