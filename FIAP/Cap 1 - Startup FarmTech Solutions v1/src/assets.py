from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets: Bundle) -> Bundle:
    assets.auto_build = True
    assets.debug = False
    common_style_bundle = Bundle(
        "src/less/*.less",
        filters="less,cssmin",
        output="dist/css/style.css",
        extra={"rel": "stylesheet/less"},
    )
    home_style_bundle = Bundle(
        "home/less/home.less",
        filters="less,cssmin",
        output="dist/css/home.css",
        extra={"rel": "stylesheet/less"},
    )
    plantio_style_bundle = Bundle(
        "plantio/less/*.less",
        filters="less,cssmin",
        output="dist/css/plantio.css",
        extra={"rel": "stylesheet/less"},
    )
    geometria_style_bundle = Bundle(
        "geometria/less/*.less",
        filters="less,cssmin",
        output="dist/css/geometria.css",
        extra={"rel": "stylesheet/less"},
    )
    meteorologia_style_bundle = Bundle(
        "meteorologia/less/*.less",
        filters="less,cssmin",
        output="dist/css/meteorologia.css",
        extra={"rel": "stylesheet/less"},
    )
    assets.register("common_style_bundle", common_style_bundle)
    assets.register("home_style_bundle", home_style_bundle)
    assets.register("plantio_style_bundle", plantio_style_bundle)
    assets.register("geometria_style_bundle", geometria_style_bundle)
    assets.register("meteorologia_style_bundle", meteorologia_style_bundle)
    if app.config["ENVIRONMENT"] == "homolog":
        common_style_bundle.build()
        home_style_bundle.build()
        plantio_style_bundle.build()
        geometria_style_bundle.build()
    return assets