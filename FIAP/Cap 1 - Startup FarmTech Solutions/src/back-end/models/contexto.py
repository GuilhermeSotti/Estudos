class Contexto:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"Contexto(nome={self.nome}, descricao={self.descricao})"