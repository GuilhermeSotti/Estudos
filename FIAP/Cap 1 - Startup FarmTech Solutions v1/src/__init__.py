from flask import Flask
from flask_assets import Environment


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from .assets import compile_static_assets
        from .home import home
        from .geometria import geometria
        from .plantio import plantio
        from .meteorologia import meteorologia

        app.register_blueprint(home.blueprint)
        app.register_blueprint(geometria.blueprint)
        app.register_blueprint(plantio.blueprint)
        app.register_blueprint(meteorologia.blueprint)

        compile_static_assets(assets)

        return app