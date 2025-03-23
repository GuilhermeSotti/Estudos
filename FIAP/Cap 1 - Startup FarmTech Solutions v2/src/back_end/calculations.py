import math

def calcular_area_retangular(comprimento, largura):
    return comprimento * largura

def calcular_area_circular(raio):
    return math.pi * (raio ** 2)

def calcular_insumo_cafe(area, dose):
    return area * dose

def calcular_insumo_soja(num_ruas, comprimento_medio, taxa=500):
    total_metros = num_ruas * comprimento_medio
    total_mL = total_metros * taxa
    return total_mL / 1000
