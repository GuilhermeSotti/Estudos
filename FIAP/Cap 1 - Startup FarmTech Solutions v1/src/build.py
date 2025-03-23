import json

from flask import Flask

def fetch_culturas(app: Flask) -> dict:
    cultura_data_filepath = app.config["CULTURA_DATA_FILEPATH"]
    with open(cultura_data_filepath, encoding="utf-8") as file:
        culturas_data = json.load(file)
        return culturas_data