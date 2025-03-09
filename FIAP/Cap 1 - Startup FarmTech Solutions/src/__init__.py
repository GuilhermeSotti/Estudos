from flask import Flask
from flask_assets import Environment


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from .assets import compile_static_assets
        from .cultura import cultura
        from .plantio import plantio

        app.register_blueprint(cultura.blueprint)
        app.register_blueprint(plantio.blueprint)

        compile_static_assets(assets)

        return app