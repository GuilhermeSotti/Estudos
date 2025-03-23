import json

registros = []

def adicionar_registro(registro):
    registros.append(registro)

def listar_registros():
    return registros

def atualizar_registro(indice, novo_registro):
    if 0 <= indice < len(registros):
        registros[indice] = novo_registro
        return True
    return False

def deletar_registro(indice):
    if 0 <= indice < len(registros):
        registros.pop(indice)
        return True
    return False


def exportar_dados_json(caminho='data/dados_farmtech.json'):
    registros = listar_registros()
    # Converter objetos para dicionários, se necessário. Exemplo:
    registros_convertidos = []
    for reg in registros:
        registros_convertidos.append({
            'cultura': reg.nome,
            'formato': reg.formato,
            'dimensoes': reg.dimensoes,
            'area': reg.area,
            'insumo': {
                'produto': reg.insumo.produto,
                'dose': reg.insumo.dose,
                'quantidade': reg.insumo.quantidade,
                'extras': reg.insumo.extras
            }
        })
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(registros_convertidos, f, ensure_ascii=False, indent=4)
    print(f"Dados exportados para {caminho}")