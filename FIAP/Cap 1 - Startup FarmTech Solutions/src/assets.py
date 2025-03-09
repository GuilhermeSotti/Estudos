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
    plantio_style_bundle = Bundle(
        "plantio/less/plantio.less",
        filters="less,cssmin",
        output="dist/css/plantio.css",
        extra={"rel": "stylesheet/less"},
    )
    cultura_style_bundle = Bundle(
        "cultura/less/cultura.less",
        filters="less,cssmin",
        output="dist/css/cultura.css",
        extra={"rel": "stylesheet/less"},
    )
    assets.register("common_style_bundle", common_style_bundle)
    assets.register("plantio_style_bundle", plantio_style_bundle)
    assets.register("cultura_style_bundle", cultura_style_bundle)
    if app.config["ENVIRONMENT"] == "homolog":
        common_style_bundle.build()
        plantio_style_bundle.build()
        cultura_style_bundle.build()
    return assets