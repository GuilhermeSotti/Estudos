from flask import Blueprint, render_template, request, current_app as app
from src.back_end.constants.geometria import Geometria

blueprint = Blueprint('geometria', __name__, template_folder=app.config["TEMPLATES_FOLDER"], static_folder=app.config["STATIC_FOLDER"])

@blueprint.route("/area/<string:forma>", methods=["GET"])
def area(forma):
    valores = request.form.getlist("valores")
    valores = [float(v) for v in valores if v]

    try:
        forma_enum = Geometria[forma.upper()]
        resultado = forma_enum.calcular_area(*valores)
        return render_template("resultado.jinja2", tipo="Área", forma=forma_enum.nome, resultado=resultado)
    except (KeyError, TypeError, ValueError) as e:
        return render_template("resultado.jinja2", erro=str(e))

@blueprint.route("/perimetro/<string:forma>/<float:distancia>", methods=["GET"])
def perimetro(forma, distancia):
    try:
        forma_enum = Geometria[forma.upper()]
        resultado = forma_enum.calcular_perimetro(distancia)
        return render_template("resultado.jinja2", tipo="Perímetro", forma=forma_enum.nome, resultado=resultado)
    except KeyError:
        return render_template("resultado.jinja2", erro="Forma geométrica inválida!")
