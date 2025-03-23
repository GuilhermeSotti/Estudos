from enum import Enum

class TipoCultura(Enum):
    def __init__(self, valor, producao_anual, preco_venda_unitaria, quantidade_lote, venda_em_lote, temporada, densidade, gasto_agua, gasto_energia, gasto_maquina, gasto_mao_obra):
        self.valor = valor
        self.producao_anual = producao_anual
        self.producao_mensal = int(producao_anual / 12)
        self.preco_venda_unitaria = preco_venda_unitaria
        self.quantidade_lote = quantidade_lote
        self.venda_em_lote = venda_em_lote
        self.temporada = temporada
        self.densidade = densidade
        self.gasto_agua = gasto_agua
        self.gasto_energia = gasto_energia
        self.gasto_maquina = gasto_maquina
        self.gasto_mao_obra = gasto_mao_obra
    
    def calcular_produtividade_media(self, area):
        return self.producao_anual / area
    
    def calcular_retorno_unitario(self, quantidade):
        return quantidade * self.preco_venda_unitaria

    def calcular_retorno_lote(self, quantidade):
        return quantidade * (self.venda_em_lote * self.quantidade_lote)

class Planta(TipoCultura):
    AVEIA = (0.03, 2, 1, 3.000000, 0.8, 'inverno', 0.0033, 500, 400, 1.000, 5.000, 0.00006, 0.0000035, 0.002)
    BANANA = (7, 1, 3, 2.000, 2.4, 'verao', 5, 1.200, 800, 2.500, 8.000, 0.40, 0.0008, 0.0009)
    TRIGO = (0.02, 2, 1, 2.500000, 0.7, 'primavera', 0.004, 600, 500, 1.500, 6.000, 0.000104, 0.0000035, 0.001)

    def __init__(self, valor, producao_anual, preco_venda_unitaria, quantidade_lote, venda_em_lote, temporada, densidade, gasto_agua, gasto_energia, gasto_maquina, gasto_mao_obra, dose_fertilizante, dose_defensivo, indice_germiniacao):
        super().__init__(valor, producao_anual, preco_venda_unitaria, quantidade_lote, venda_em_lote, temporada, densidade, gasto_agua, gasto_energia, gasto_maquina, gasto_mao_obra)
        self.dose_fertilizante = dose_fertilizante
        self.dose_defensivo = dose_defensivo
        self.indice_germiniacao = indice_germiniacao

    def calcular_gastos(self, area):
        return (self.dose_fertilizante + self.dose_defensivo) * area

    def calcular_ganhos(self, area):
        return self.calcular_retorno_unitario(self.producao_anual) - self.calcular_gastos(area)

    def calcular_custo_insumos(self, area):
        insumos = {
            "dose_fertilizante": self.dose_fertilizante * area,
            "dose_defensivo": self.dose_defensivo * area
        }
        return sum(insumos.values())
    
    def calcular_consumo_agua(self, area):
        return self.gasto_agua * area
    
    def calcular_consumo_energia(self, area):
        return self.gasto_energia * area   
    
    def calcular_consumo_maquina(self, area):
        return self.gasto_maquina * area
        
    def calcular_produtividade_mao_obra(self, area):
        return self.gasto_mao_obra * area
    
    def calcular_perdas_pos_colheita(self):
        return self.producao_anual * self.indice_germiniacao
    
    def calcular_consumo_diario(self, area):
        agua = self.calcular_consumo_agua(area)
        energia = self.calcular_consumo_energia(area)
        maquina = self.calcular_consumo_maquina(area)
        mao_obra = self.calcular_produtividade_mao_obra(area)
        return agua + energia + maquina + mao_obra
    
class Animal(TipoCultura):
    VACA = (3000, 2, 20, 200, 17, 'anual', 10, 50, 30, 400, 3.500, 0.1, 0.005, 500, 16)
    GALINHA = (4, 6, 6, 50.000, 5.5, 'anual', 0.2, 0.50, 0.05, 1, 0.13, 0.005, 0.0003, 2, 0.1)
    PORCO = (350, 3, 10, 1.000, 9.5, 'anual', 2, 12, 15, 150, 600, 0.05, 0.001, 120, 1.5)

    def __init__(self, valor, producao_anual, preco_venda_unitaria, quantidade_lote, venda_em_lote, temporada, densidade, gasto_agua, gasto_energia, gasto_maquina, gasto_mao_obra, suplemento_alimentar, medicamento, peso, consumo_diario):
        super().__init__(valor, producao_anual, preco_venda_unitaria, quantidade_lote, venda_em_lote, temporada, densidade, gasto_agua, gasto_energia, gasto_maquina, gasto_mao_obra)
        self.suplemento_alimentar = suplemento_alimentar
        self.medicamento = medicamento
        self.peso = peso
        self.consumo_diario = consumo_diario

    def calcular_gastos(self, dias):
        return (self.consumo_diario + self.suplemento_alimentar + self.medicamento) * dias

    def calcular_ganhos(self, dias):
        return self.calcular_retorno_unitario(self.producao_anual) - self.calcular_gastos(dias)
    
    def calcular_custo_insumos(self, dias):
        insumos = {
            "consumo_diario": self.consumo_diario * dias,
            "suplemento_alimentar": self.suplemento_alimentar * dias,
            "medicamento": self.medicamento * dias
        }
        return sum(insumos.values())
    
    def calcular_consumo_agua(self, dias):
        return self.gasto_agua * dias
    
    def calcular_consumo_energia(self, dias):
        return self.gasto_energia * dias
    
    def calcular_consumo_maquina(self, dias):
        return self.gasto_maquina * dias
    
    def calcular_produtividade_mao_obra(self, dias):
        return self.gasto_mao_obra * dias
    
    def calcular_consumo_diario(self, dias):
        agua = self.calcular_consumo_agua(dias)
        energia = self.calcular_consumo_energia(dias)
        maquina = self.calcular_consumo_maquina(dias)
        mao_obra = self.calcular_produtividade_mao_obra(dias)
        return agua + energia + maquina + mao_obra