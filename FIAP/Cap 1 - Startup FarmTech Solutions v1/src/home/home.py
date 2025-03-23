from flask import Blueprint, current_app as app, render_template
from src.build import fetch_culturas

blueprint = Blueprint("home", __name__, template_folder=app.config["TEMPLATES_FOLDER"], static_folder=app.config["STATIC_FOLDER"])


@blueprint.route("/", methods=["GET"])
def home() -> str:
    products = fetch_culturas(app)
    return render_template(
        "home.jinja2",
        title="Cap 1 - Startup FarmTech Solutions",
        subtitle="Culturas",
        template="home-template",
        products=products,
    )