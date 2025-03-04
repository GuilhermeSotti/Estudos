from back_end.constants.culturas import TipoCultura, Planta, Animal
from back_end.models.geometria import Geometria
import json
class Plantio:
    def __init__(self, nome, geometria, tipo, dias, area_plantada, estado, cidade):
        self.nome = nome
        self.geometria = geometria
        self.tipo = tipo
        self.dias = dias
        self.area_plantada = area_plantada
        self.estado = estado
        self.cidade = cidade

    def metricas(self):
        metricas = {
            "valor": self.tipo.valor,
            "producao_anual": self.tipo.producao_anual,
            "producao_mensal": self.tipo.producao_mensal,
            "preco_venda_unitaria": self.tipo.preco_venda_unitaria,
            "quantidade_lote": self.tipo.quantidade_lote,
            "venda_em_lote": self.tipo.venda_em_lote,
            "temporada": self.tipo.temporada,
            "densidade": self.tipo.densidade,
            "gasto_agua": self.tipo.gasto_agua,
            "gasto_energia": self.tipo.gasto_energia,
            "gasto_maquina": self.tipo.gasto_maquina,
            "gasto_mao_obra": self.tipo.gasto_mao_obra,
        }

        if isinstance(self.tipo, Planta):
            metricas.update({
                "dose_fertilizante": self.tipo.dose_fertilizante,
                "dose_defensivo": self.tipo.dose_defensivo,
                "gastos": self.tipo.calcular_gastos(self.area_plantada),
                "ganhos": self.tipo.calcular_ganhos(self.tipo.producao_anual),
                "custo_insumos": self.tipo.calcular_custo_insumos(self.area_plantada),
                "consumo_agua": self.tipo.calcular_consumo_agua(self.area_plantada),
                "consumo_energia": self.tipo.calcular_consumo_energia(self.area_plantada),
                "consumo_maquina": self.tipo.calcular_consumo_maquina(self.area_plantada),
                "produtividade_mao_obra": self.tipo.calcular_produtividade_mao_obra(self.area_plantada),
                "perdas_pos_colheita": self.tipo.calcular_perdas_pos_colheita(),
                "consumo_diario": self.tipo.calcular_consumo_diario(self.area_plantada),
            })

        elif isinstance(self.tipo, Animal):
            metricas.update({
                "suplemento_alimentar": self.tipo.suplemento_alimentar,
                "medicamento": self.tipo.medicamento,
                "peso": self.tipo.peso,
                "gastos": self.tipo.calcular_gastos(self.dias),
                "ganhos": self.tipo.calcular_ganhos(self.dias),
                "custo_insumos": self.tipo.calcular_custo_insumos(self.dias),
                "consumo_agua": self.tipo.calcular_consumo_agua(self.dias),
                "consumo_energia": self.tipo.calcular_consumo_energia(self.dias),
                "consumo_maquina": self.tipo.calcular_consumo_maquina(self.dias),
                "produtividade_mao_obra": self.tipo.calcular_produtividade_mao_obra(self.dias),
                "consumo_diario": self.tipo.calcular_consumo_diario(self.dias),
            })

        return json.dumps(metricas, indent=4)

    def insumos(self):
        if isinstance(self.tipo, Planta):
            insumos = self.tipo.calcular_custo_insumos(self.area_plantada)
        elif isinstance(self.tipo, Animal):
            insumos = self.tipo.calcular_custo_insumos(self.dias)

        return {"insumos": insumos}
    
    def eficiencia(self):
        if isinstance(self.tipo, Planta):
            producao_media = self.tipo.calcular_produtividade_media(self.area_plantada)
            custo_total = self.tipo.calcular_gastos(self.area_plantada)
        elif isinstance(self.tipo, Animal):
            producao_media = self.tipo.calcular_produtividade_media(self.dias)
            custo_total = self.tipo.calcular_gastos(self.dias)
        
        eficiencia = producao_media / custo_total if custo_total > 0 else 0
        return {"eficiencia": eficiencia}
    
    def rentabilidade(self):

        if isinstance(self.tipo, Planta):
            ganhos = self.tipo.calcular_ganhos(self.area_plantada)
            gastos = self.tipo.calcular_gastos(self.area_plantada)
        elif isinstance(self.tipo, Animal):
            ganhos = self.tipo.calcular_ganhos(self.dias)
            gastos = self.tipo.calcular_gastos(self.dias)
    
        rentabilidade = (ganhos - gastos) / gastos if gastos > 0 else 0
        return {"rentabilidade": rentabilidade}