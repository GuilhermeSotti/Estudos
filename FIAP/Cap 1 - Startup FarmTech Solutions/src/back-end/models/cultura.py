class Cultura:
    def __init__(self, nome, tipo, area_plantada, producao_anual):
        self.nome = nome
        self.tipo = tipo
        self.area_plantada = area_plantada
        self.producao_anual = producao_anual

    def __repr__(self):
        return f"Cultura(nome={self.nome}, tipo={self.tipo}, area_plantada={self.area_plantada}, producao_anual={self.producao_anual})"