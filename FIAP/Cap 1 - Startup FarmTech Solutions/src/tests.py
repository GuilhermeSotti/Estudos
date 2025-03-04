import unittest
import json

from back_end.models.geometria import Geometria
from back_end.constants.perimetros import Perimetro
from back_end.controller.plantio import Plantio
from back_end.constants.culturas import Planta, Animal
class TestGeometria(unittest.TestCase):

    def test_quantidade_area_cultivavel(self):
        
        geometria = Geometria(Perimetro.QUADRADO)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, terreno=2)
        self.assertEqual(area_cultivavel, 50)

        geometria = Geometria(Perimetro.RETANGULO)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, 20, terreno=1.5)
        self.assertEqual(area_cultivavel, 133)

        geometria = Geometria(Perimetro.TRIANGULO)
        area_cultivavel = geometria.quantidade_area_cultivavel(10, 20, terreno=1)
        self.assertEqual(area_cultivavel, 100)

    def test_calcular_perimetro(self):
        geometria = Geometria(Perimetro.QUADRADO)
        perimetro_calculado = geometria.perimetro.calcular_perimetro(10)
        self.assertEqual(perimetro_calculado, 40)

        geometria = Geometria(Perimetro.RETANGULO)
        perimetro_calculado = geometria.perimetro.calcular_perimetro(10)
        self.assertEqual(perimetro_calculado, 40)

        geometria = Geometria(Perimetro.TRIANGULO)
        perimetro_calculado = geometria.perimetro.calcular_perimetro(10)
        self.assertEqual(perimetro_calculado, 30)

class TestPlantio(unittest.TestCase):

    def setUp(self):
        self.geometria = Geometria(Perimetro.QUADRADO)
        self.planta = Plantio("Planta1", self.geometria, Planta.AVEIA, 100, 50, "SP", "São Paulo")
        self.animal = Plantio("Animal1", self.geometria, Animal.VACA, 200, 100, "MG", "Belo Horizonte")

    def test_metricas_planta(self):
        metricas = self.planta.metricas()
        metricas_dict = json.loads(metricas)

        self.assertEqual(metricas_dict["valor"], 0.03)
        self.assertEqual(metricas_dict["producao_anual"], 2)
        self.assertEqual(metricas_dict["dose_fertilizante"], 0.00006)
        self.assertEqual(metricas_dict["gastos"], 0.003175)
        self.assertEqual(metricas_dict["ganhos"], 1.999873)

    def test_metricas_animal(self):
        metricas = self.animal.metricas()
        metricas_dict = json.loads(metricas)

        self.assertEqual(metricas_dict["valor"], 3000)
        self.assertEqual(metricas_dict["producao_anual"], 2)
        self.assertEqual(metricas_dict["suplemento_alimentar"], 0.1)
        self.assertEqual(metricas_dict["gastos"], 3221.0)
        self.assertEqual(metricas_dict["ganhos"], -3181.0)

if __name__ == "__main__":
    unittest.main()