from back_end.constants.perimetros import Perimetro

import math

class Geometria:

    def __init__(self, tipo):
        self.perimetro = Perimetro(tipo)

    def quantidade_area_cultivavel(self, *distancias, terreno):
        area = self.perimetro.calcular_area(*distancias)
        return math.floor(area / terreno)
