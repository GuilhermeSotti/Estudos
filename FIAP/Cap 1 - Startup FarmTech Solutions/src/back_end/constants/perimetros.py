from enum import Enum
import math

class Perimetro(Enum):
    QUADRADO = ("Quadrado", 4)
    TRIANGULO = ("Triângulo", 3)
    CIRCULO = ("Círculo", 0)
    RETANGULO = ("Retângulo", 4)
    PENTAGONO = ("Pentágono", 5)
    HEXAGONO = ("Hexágono", 6)

    def __init__(self, nome, lados):
        self.nome = nome
        self.lados = lados

    def calcular_area(self, *args):
        def area_quadrado(lado):
            return lado * lado

        def area_retangulo(base, altura):
            return base * altura

        def area_triangulo(base, altura):
            return (base * altura) / 2

        def area_circulo(raio):
            return math.pi * (raio ** 2)

        def area_pentagono(lado):
            return (5 * lado ** 2) / (4 * math.tan(math.pi / 5))

        def area_hexagono(lado):
            return (3 * math.sqrt(3) * lado ** 2) / 2

        if self == Perimetro.QUADRADO:
            return area_quadrado(*args)
        elif self == Perimetro.RETANGULO:
            return area_retangulo(*args)
        elif self == Perimetro.TRIANGULO:
            return area_triangulo(*args)
        elif self == Perimetro.CIRCULO:
            return area_circulo(*args)
        elif self == Perimetro.PENTAGONO:
            return area_pentagono(*args)
        elif self == Perimetro.HEXAGONO:
            return area_hexagono(*args)

    def calcular_perimetro(self, distancia):
        return self.lados * distancia