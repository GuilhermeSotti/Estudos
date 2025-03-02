import unittest

from back_end.models.geometria import Geometria
from back_end.constants.perimetros import Perimetro

class TestGeometria(unittest.TestCase):

    def test_quantidade_area_cultivavel(self):
        
        perimetro = Perimetro.QUADRADO
        geometria = Geometria(perimetro)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, terreno=2)
        self.assertEqual(area_cultivavel, 50)

        perimetro = Perimetro.RETANGULO
        geometria = Geometria(perimetro)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, 20, terreno=1.5)
        self.assertEqual(area_cultivavel, 133)

        perimetro = Perimetro.TRIANGULO
        geometria = Geometria(perimetro)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, 20, terreno=1)
        self.assertEqual(area_cultivavel, 100)

if __name__ == "__main__":
    unittest.main()