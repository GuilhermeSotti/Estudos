from src.back_end.models import Cultura
import json
import os

CAMINHO_JSON = "FIAP\\Cap 1 - Startup FarmTech Solutions v2\\data\\dados_farmtech.json"

registros = []

def carregar_dados():
    global registros
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            registros = json.load(f)
    else:
        registros = []

def salvar_dados():
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {CAMINHO_JSON}")

def adicionar_registro(cultura):
    if isinstance(cultura, Cultura):
        registros.append(cultura.to_dict())
        salvar_dados()
    else:
        print("O objeto precisa ser uma instância de Cultura!")

def listar_registros():
    return registros

def atualizar_registro(indice, novo_registro):
    if 0 <= indice < len(registros):
        registros[indice] = novo_registro
        salvar_dados()
        return True
    return False

def deletar_registro(indice):
    if 0 <= indice < len(registros):
        registros.pop(indice)
        salvar_dados()
        return True
    return False

carregar_dados()