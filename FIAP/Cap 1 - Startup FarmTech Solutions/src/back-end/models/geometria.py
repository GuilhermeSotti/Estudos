import math
import math

class Geometria:
    def __init__(self, tipo, dimensoes):
        self.tipo = tipo
        self.dimensoes = dimensoes

    def area(self):
        if self.tipo == 'quadrado':
            return self.dimensoes['lado'] ** 2
        elif self.tipo == 'retangulo':
            return self.dimensoes['largura'] * self.dimensoes['altura']
        elif self.tipo == 'circulo':
            return math.pi * (self.dimensoes['raio'] ** 2)
        else:
            raise ValueError("Tipo de geometria não suportado")

    def perimetro(self):
        if self.tipo == 'quadrado':
            return 4 * self.dimensoes['lado']
        elif self.tipo == 'retangulo':
            return 2 * (self.dimensoes['largura'] + self.dimensoes['altura'])
        elif self.tipo == 'circulo':
            return 2 * math.pi * self.dimensoes['raio']
        else:
            raise ValueError("Tipo de geometria não suportado")