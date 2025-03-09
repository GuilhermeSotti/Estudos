from flask import Blueprint, jsonify, request, render_template
from back_end.constants.culturas import Planta, Animal
from back_end.utils.log import log_execution
import json
blueprint = Blueprint('plantio', __name__, template_folder="templates", static_folder="static")

@log_execution("Calculando métricas do plantio")
@blueprint.route("/metricas/<str:nome>", methods=["GET"])
def metricas(nome: str):
    plantio = obter_plantio(nome)
    metricas = {
        "valor": plantio.tipo.valor,
        "producao_anual": plantio.tipo.producao_anual,
        "producao_mensal": plantio.tipo.producao_mensal,
        "preco_venda_unitaria": plantio.tipo.preco_venda_unitaria,
        "quantidade_lote": plantio.tipo.quantidade_lote,
        "venda_em_lote": plantio.tipo.venda_em_lote,
        "temporada": plantio.tipo.temporada,
        "densidade": plantio.tipo.densidade,
        "gasto_agua": plantio.tipo.gasto_agua,
        "gasto_energia": plantio.tipo.gasto_energia,
        "gasto_maquina": plantio.tipo.gasto_maquina,
        "gasto_mao_obra": plantio.tipo.gasto_mao_obra,
    }

    if isinstance(plantio.tipo, Planta):
        metricas.update({
            "dose_fertilizante": plantio.tipo.dose_fertilizante,
            "dose_defensivo": plantio.tipo.dose_defensivo,
            "gastos": plantio.tipo.calcular_gastos(plantio.area_plantada),
            "ganhos": plantio.tipo.calcular_ganhos(plantio.tipo.producao_anual),
            "custo_insumos": plantio.tipo.calcular_custo_insumos(plantio.area_plantada),
            "consumo_agua": plantio.tipo.calcular_consumo_agua(plantio.area_plantada),
            "consumo_energia": plantio.tipo.calcular_consumo_energia(plantio.area_plantada),
            "consumo_maquina": plantio.tipo.calcular_consumo_maquina(plantio.area_plantada),
            "produtividade_mao_obra": plantio.tipo.calcular_produtividade_mao_obra(plantio.area_plantada),
            "perdas_pos_colheita": plantio.tipo.calcular_perdas_pos_colheita(),
            "consumo_diario": plantio.tipo.calcular_consumo_diario(plantio.area_plantada),
        })

    elif isinstance(plantio.tipo, Animal):
        metricas.update({
            "suplemento_alimentar": plantio.tipo.suplemento_alimentar,
            "medicamento": plantio.tipo.medicamento,
            "peso": plantio.tipo.peso,
            "gastos": plantio.tipo.calcular_gastos(plantio.dias),
            "ganhos": plantio.tipo.calcular_ganhos(plantio.dias),
            "custo_insumos": plantio.tipo.calcular_custo_insumos(plantio.dias),
            "consumo_agua": plantio.tipo.calcular_consumo_agua(plantio.dias),
            "consumo_energia": plantio.tipo.calcular_consumo_energia(plantio.dias),
            "consumo_maquina": plantio.tipo.calcular_consumo_maquina(plantio.dias),
            "produtividade_mao_obra": plantio.tipo.calcular_produtividade_mao_obra(plantio.dias),
            "consumo_diario": plantio.tipo.calcular_consumo_diario(plantio.dias),
        })

    return render_template("metricas.jinja2", title="Métricas", metricas=metricas)

@log_execution("Calculando insumos do plantio")
@blueprint.route("/insumos/<string:nome>", methods=["GET"])
def insumos(nome: str):
    plantio = obter_plantio(nome)
    if isinstance(plantio.tipo, Planta):
        insumos = plantio.tipo.calcular_custo_insumos(plantio.area_plantada)
    elif isinstance(plantio.tipo, Animal):
        insumos = plantio.tipo.calcular_custo_insumos(plantio.dias)

    return render_template("insumos.jinja2", title="Insumos", insumos=insumos)

@log_execution("Calculando eficiência do plantio")
@blueprint.route("/eficiencia/<string:nome>", methods=["GET"])
def eficiencia(nome: str):
    plantio = obter_plantio(nome)
    if isinstance(plantio.tipo, Planta):
        producao_media = plantio.tipo.calcular_produtividade_media(plantio.area_plantada)
        custo_total = plantio.tipo.calcular_gastos(plantio.area_plantada)
    elif isinstance(plantio.tipo, Animal):
        producao_media = plantio.tipo.calcular_produtividade_media(plantio.dias)
        custo_total = plantio.tipo.calcular_gastos(plantio.dias)
    
    eficiencia = producao_media / custo_total if custo_total > 0 else 0
    return render_template("eficiencia.jinja2", title="Eficiência", eficiencia=eficiencia)

@log_execution("Calculando rentabilidade do plantio")
@blueprint.route("/rentabilidade/<string:nome>", methods=["GET"])
def rentabilidade(nome: str):
    plantio = obter_plantio(nome)
    if isinstance(plantio.tipo, Planta):
        ganhos = plantio.tipo.calcular_ganhos(plantio.area_plantada)
        gastos = plantio.tipo.calcular_gastos(plantio.area_plantada)
    elif isinstance(plantio.tipo, Animal):
        ganhos = plantio.tipo.calcular_ganhos(plantio.dias)
        gastos = plantio.tipo.calcular_gastos(plantio.dias)

    rentabilidade = (ganhos - gastos) / gastos if gastos > 0 else 0
    return render_template("rentabilidade.jinja2", title="Rentabilidade", rentabilidade=rentabilidade)

@log_execution("Cadastrando novo plantio")
@blueprint.route("/cadastro", methods=["POST"])
def cadastro():
    try:
        dados = request.json
        
        if not dados:
            return render_template("resposta.jinja2", erro="Nenhum dado enviado!")

        nome = dados.get("nome")
        tipo = dados.get("tipo")
        area_plantada = dados.get("area_plantada", 0)
        dias = dados.get("dias", 0)

        if not nome or not tipo:
            return render_template("resposta.jinja2", erro="Nome e tipo são obrigatórios!")

        if tipo.upper() in Planta.__members__:
            tipo_cultura = Planta[tipo.upper()]
            novo_plantio = {
                "nome": nome,
                "tipo": tipo,
                "area_plantada": area_plantada,
                "dose_fertilizante": tipo_cultura.dose_fertilizante,
                "dose_defensivo": tipo_cultura.dose_defensivo,
                "indice_germinacao": tipo_cultura.indice_germiniacao
            }
        elif tipo.upper() in Animal.__members__:
            tipo_cultura = Animal[tipo.upper()]
            novo_plantio = {
                "nome": nome,
                "tipo": tipo,
                "dias": dias,
                "suplemento_alimentar": tipo_cultura.suplemento_alimentar,
                "medicamento": tipo_cultura.medicamento,
                "peso": tipo_cultura.peso,
                "consumo_diario": tipo_cultura.consumo_diario
            }

        try:
            with open('data/plantios.json', 'r') as arquivo:
                plantios = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            plantios = []

        plantios.append(novo_plantio)

        with open('data/plantios.json', 'w') as arquivo:
            json.dump(plantios, arquivo, indent=4)

        return render_template("resposta.jinja2", mensagem="Plantio cadastrado com sucesso!", plantios=plantios)

    except Exception as e:
        return render_template("resposta.jinja2", erro=str(e))

@log_execution("Obtendo plantio")
def obter_plantio(nome: str):
    with open('data/plantios.json') as json:
        plantios = json.load(json)

    for plantio in plantios:
        if plantio.nome == nome:
            return plantio.__dict__
    return jsonify({"mensagem": "Objeto não encontrado!"})