from flask import Blueprint, request, render_template, current_app as app
import requests

blueprint = Blueprint('meteorologia', __name__, template_folder=app.config["TEMPLATES_FOLDER"], static_folder=app.config["STATIC_FOLDER"])

@blueprint.route("/clima", methods=["GET"])
def clima():
    city = request.args.get("city", app.config["DEFAULT_CITY"])
    weather_data = get_meteorologia(city)
    return render_template("weather.jinja2", weather=weather_data, city=city)

def get_meteorologia(city):
    params = {
        "q": city,
        "appid": app.config["API_KEY"],
        "units": "metric",
        "lang": "pt"
    }
    response = requests.get(app.config["API_URL"], params=params)
    
    if response.status_code == 200:
        return response.json()
    return None